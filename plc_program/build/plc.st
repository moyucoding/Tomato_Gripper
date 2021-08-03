TYPE
  LOGLEVEL : (CRITICAL, WARNING, INFO, DEBUG) := INFO;
END_TYPE

FUNCTION_BLOCK LOGGER
  VAR_INPUT
    TRIG : BOOL;
    MSG : STRING;
    LEVEL : LOGLEVEL := INFO;
  END_VAR
  VAR
    TRIG0 : BOOL;
  END_VAR

  IF TRIG AND NOT TRIG0 THEN
  {{
   LogMessage(GetFbVar(LEVEL),(char*)GetFbVar(MSG, .body),GetFbVar(MSG, .len));
  }}
  END_IF;
  TRIG0:=TRIG;
END_FUNCTION_BLOCK



FUNCTION_BLOCK python_eval
  VAR_INPUT
    TRIG : BOOL;
    CODE : STRING;
  END_VAR
  VAR_OUTPUT
    ACK : BOOL;
    RESULT : STRING;
  END_VAR
  VAR
    STATE : DWORD;
    BUFFER : STRING;
    PREBUFFER : STRING;
    TRIGM1 : BOOL;
    TRIGGED : BOOL;
  END_VAR

  {extern void __PythonEvalFB(int, PYTHON_EVAL*);__PythonEvalFB(0, data__);}
END_FUNCTION_BLOCK

FUNCTION_BLOCK python_poll
  VAR_INPUT
    TRIG : BOOL;
    CODE : STRING;
  END_VAR
  VAR_OUTPUT
    ACK : BOOL;
    RESULT : STRING;
  END_VAR
  VAR
    STATE : DWORD;
    BUFFER : STRING;
    PREBUFFER : STRING;
    TRIGM1 : BOOL;
    TRIGGED : BOOL;
  END_VAR

  {extern void __PythonEvalFB(int, PYTHON_EVAL*);__PythonEvalFB(1,(PYTHON_EVAL*)(void*)data__);}
END_FUNCTION_BLOCK

FUNCTION_BLOCK python_gear
  VAR_INPUT
    N : UINT;
    TRIG : BOOL;
    CODE : STRING;
  END_VAR
  VAR_OUTPUT
    ACK : BOOL;
    RESULT : STRING;
  END_VAR
  VAR
    py_eval : python_eval;
    COUNTER : UINT;
    ADD10_OUT : UINT;
    EQ13_OUT : BOOL;
    SEL15_OUT : UINT;
    AND7_OUT : BOOL;
  END_VAR

  ADD10_OUT := ADD(COUNTER, 1);
  EQ13_OUT := EQ(N, ADD10_OUT);
  SEL15_OUT := SEL(EQ13_OUT, ADD10_OUT, 0);
  COUNTER := SEL15_OUT;
  AND7_OUT := AND(EQ13_OUT, TRIG);
  py_eval(TRIG := AND7_OUT, CODE := CODE);
  ACK := py_eval.ACK;
  RESULT := py_eval.RESULT;
END_FUNCTION_BLOCK


FUNCTION_BLOCK MoveArm
  VAR_INPUT
    ENABLE : BOOL := FALSE;
    SPEED : SINT := 0;
    TARGET : STRING := '0,0,0,0,0,0,0';
  END_VAR
  VAR_OUTPUT
    VALID : BOOL := FALSE;
    ERROR : BOOL := FALSE;
    ERRORCODE : SINT := 0;
  END_VAR
  VAR
    WAIT : SINT := 0;
  END_VAR

  {{
    int wait = GetFbVar(WAIT);
    bool enable = GetFbVar(ENABLE);
    int fd = open("/tmp/ArmControl.pipe",O_RDWR | O_NONBLOCK);
    if(wait==0 && enable){
      SetFbVar(WAIT, 1);
    }
    else if(wait == 1){
      char buf[200] = {"movePos;"};
      //SPEED
      int speed = GetFbVar(SPEED);
      strcat(buf, "1");
      //char *word = GetFbVar(TARGET).body;
      //sprintf(word, "%d", speed);
      //strcat(buf,word);
      strcat(buf,",");
      //Target
      char *word1 = GetFbVar(TARGET).body;
      strcat(buf,word1);
      strcat(buf,";");
      
      int ret = write(fd, buf, 200);
      if(ret > 0){
        SetFbVar(WAIT, 2);
      }
    }
    else if(wait == 2){
      char buf[200];
      int ret = read(fd, buf, 200);
      if(ret>0){
        if(buf[0]=='n'){
          //ERROR
          SetFbVar(ERROR, true);
          //1-digit error id
          SetFbVar(ERRORCODE, buf[1] - 48);
          SetFbVar(WAIT, 3);
        }
        else if(buf[0] == 'Y' && buf[2] == 'm' ){
          SetFbVar(VALID, true);
          SetFbVar(WAIT, 3);
        }
        else{
          write(fd, buf, 200);
        }
      }
    }
    else if((wait == 3) && !enable){
      
      SetFbVar(VALID, false);
      SetFbVar(ERROR, false);
      SetFbVar(ERRORCODE, 0);
      SetFbVar(WAIT, 0);
    }
    close(fd);
  }}
END_FUNCTION_BLOCK

PROGRAM program0
  VAR
    SWITCH : BOOL;
    COUNTER : LINT := 0;
    ONE : LINT := 1;
    SPEED : SINT := 1;
    TARGET1 : STRING := '219.91,-332.00,289.34,0.21,0.66,-0.65,0.32';
    TARGET2 : STRING := '636.63,138.27,410.64,0.12,-0.72,0.07,-0.68';
    R_TRIG0 : R_TRIG;
    functionBlock1 : MoveArm;
    functionBlock0 : MoveArm;
    R_TRIG1 : R_TRIG;
    OR8_OUT : BOOL;
    ADD11_ENO : BOOL;
    ADD11_OUT : LINT;
  END_VAR

  functionBlock1(ENABLE := functionBlock0.VALID, SPEED := SPEED, TARGET := TARGET2);
  R_TRIG0(CLK := SWITCH);
  OR8_OUT := OR(functionBlock1.VALID, R_TRIG0.Q);
  functionBlock0(ENABLE := OR8_OUT, SPEED := SPEED, TARGET := TARGET1);
  R_TRIG1(CLK := functionBlock0.VALID OR functionBlock1.VALID);
  ADD11_OUT := ADD(EN := R_TRIG1.Q, IN1 := ONE, IN2 := COUNTER, ENO => ADD11_ENO);
  IF ADD11_ENO THEN
      COUNTER := ADD11_OUT;
  END_IF;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION
