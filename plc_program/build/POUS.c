void LOGGER_init__(LOGGER *data__, BOOL retain) {
  __INIT_VAR(data__->EN,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->ENO,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->TRIG,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->MSG,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->LEVEL,LOGLEVEL__INFO,retain)
  __INIT_VAR(data__->TRIG0,__BOOL_LITERAL(FALSE),retain)
}

// Code part
void LOGGER_body__(LOGGER *data__) {
  // Control execution
  if (!__GET_VAR(data__->EN)) {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(FALSE));
    return;
  }
  else {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(TRUE));
  }
  // Initialise TEMP variables

  if ((__GET_VAR(data__->TRIG,) && !(__GET_VAR(data__->TRIG0,)))) {
    #define GetFbVar(var,...) __GET_VAR(data__->var,__VA_ARGS__)
    #define SetFbVar(var,val,...) __SET_VAR(data__->,var,__VA_ARGS__,val)

   LogMessage(GetFbVar(LEVEL),(char*)GetFbVar(MSG, .body),GetFbVar(MSG, .len));
  
    #undef GetFbVar
    #undef SetFbVar
;
  };
  __SET_VAR(data__->,TRIG0,,__GET_VAR(data__->TRIG,));

  goto __end;

__end:
  return;
} // LOGGER_body__() 





void PYTHON_EVAL_init__(PYTHON_EVAL *data__, BOOL retain) {
  __INIT_VAR(data__->EN,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->ENO,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->TRIG,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->CODE,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->ACK,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->RESULT,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->STATE,0,retain)
  __INIT_VAR(data__->BUFFER,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->PREBUFFER,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->TRIGM1,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->TRIGGED,__BOOL_LITERAL(FALSE),retain)
}

// Code part
void PYTHON_EVAL_body__(PYTHON_EVAL *data__) {
  // Control execution
  if (!__GET_VAR(data__->EN)) {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(FALSE));
    return;
  }
  else {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(TRUE));
  }
  // Initialise TEMP variables

  #define GetFbVar(var,...) __GET_VAR(data__->var,__VA_ARGS__)
  #define SetFbVar(var,val,...) __SET_VAR(data__->,var,__VA_ARGS__,val)
extern void __PythonEvalFB(int, PYTHON_EVAL*);__PythonEvalFB(0, data__);
  #undef GetFbVar
  #undef SetFbVar
;

  goto __end;

__end:
  return;
} // PYTHON_EVAL_body__() 





void PYTHON_POLL_init__(PYTHON_POLL *data__, BOOL retain) {
  __INIT_VAR(data__->EN,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->ENO,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->TRIG,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->CODE,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->ACK,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->RESULT,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->STATE,0,retain)
  __INIT_VAR(data__->BUFFER,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->PREBUFFER,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->TRIGM1,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->TRIGGED,__BOOL_LITERAL(FALSE),retain)
}

// Code part
void PYTHON_POLL_body__(PYTHON_POLL *data__) {
  // Control execution
  if (!__GET_VAR(data__->EN)) {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(FALSE));
    return;
  }
  else {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(TRUE));
  }
  // Initialise TEMP variables

  #define GetFbVar(var,...) __GET_VAR(data__->var,__VA_ARGS__)
  #define SetFbVar(var,val,...) __SET_VAR(data__->,var,__VA_ARGS__,val)
extern void __PythonEvalFB(int, PYTHON_EVAL*);__PythonEvalFB(1,(PYTHON_EVAL*)(void*)data__);
  #undef GetFbVar
  #undef SetFbVar
;

  goto __end;

__end:
  return;
} // PYTHON_POLL_body__() 





void PYTHON_GEAR_init__(PYTHON_GEAR *data__, BOOL retain) {
  __INIT_VAR(data__->EN,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->ENO,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->N,0,retain)
  __INIT_VAR(data__->TRIG,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->CODE,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->ACK,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->RESULT,__STRING_LITERAL(0,""),retain)
  PYTHON_EVAL_init__(&data__->PY_EVAL,retain);
  __INIT_VAR(data__->COUNTER,0,retain)
  __INIT_VAR(data__->ADD10_OUT,0,retain)
  __INIT_VAR(data__->EQ13_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->SEL15_OUT,0,retain)
  __INIT_VAR(data__->AND7_OUT,__BOOL_LITERAL(FALSE),retain)
}

// Code part
void PYTHON_GEAR_body__(PYTHON_GEAR *data__) {
  // Control execution
  if (!__GET_VAR(data__->EN)) {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(FALSE));
    return;
  }
  else {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(TRUE));
  }
  // Initialise TEMP variables

  __SET_VAR(data__->,ADD10_OUT,,ADD__UINT__UINT(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (UINT)__GET_VAR(data__->COUNTER,),
    (UINT)1));
  __SET_VAR(data__->,EQ13_OUT,,EQ__BOOL__UINT(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (UINT)__GET_VAR(data__->N,),
    (UINT)__GET_VAR(data__->ADD10_OUT,)));
  __SET_VAR(data__->,SEL15_OUT,,SEL__UINT__BOOL__UINT__UINT(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (BOOL)__GET_VAR(data__->EQ13_OUT,),
    (UINT)__GET_VAR(data__->ADD10_OUT,),
    (UINT)0));
  __SET_VAR(data__->,COUNTER,,__GET_VAR(data__->SEL15_OUT,));
  __SET_VAR(data__->,AND7_OUT,,AND__BOOL__BOOL(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (BOOL)__GET_VAR(data__->EQ13_OUT,),
    (BOOL)__GET_VAR(data__->TRIG,)));
  __SET_VAR(data__->PY_EVAL.,TRIG,,__GET_VAR(data__->AND7_OUT,));
  __SET_VAR(data__->PY_EVAL.,CODE,,__GET_VAR(data__->CODE,));
  PYTHON_EVAL_body__(&data__->PY_EVAL);
  __SET_VAR(data__->,ACK,,__GET_VAR(data__->PY_EVAL.ACK,));
  __SET_VAR(data__->,RESULT,,__GET_VAR(data__->PY_EVAL.RESULT,));

  goto __end;

__end:
  return;
} // PYTHON_GEAR_body__() 





void MOVEARM_init__(MOVEARM *data__, BOOL retain) {
  __INIT_VAR(data__->EN,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->ENO,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->ENABLE,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->SPEED,0,retain)
  __INIT_VAR(data__->TARGET,__STRING_LITERAL(13,"0,0,0,0,0,0,0"),retain)
  __INIT_VAR(data__->VALID,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->ERROR,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->ERRORCODE,0,retain)
  __INIT_VAR(data__->WAIT,0,retain)
}

// Code part
void MOVEARM_body__(MOVEARM *data__) {
  // Control execution
  if (!__GET_VAR(data__->EN)) {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(FALSE));
    return;
  }
  else {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(TRUE));
  }
  // Initialise TEMP variables

  #define GetFbVar(var,...) __GET_VAR(data__->var,__VA_ARGS__)
  #define SetFbVar(var,val,...) __SET_VAR(data__->,var,__VA_ARGS__,val)

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
  
  #undef GetFbVar
  #undef SetFbVar
;

  goto __end;

__end:
  return;
} // MOVEARM_body__() 





inline LINT __PROGRAM0_ADD__LINT__LINT1(BOOL EN,
  UINT __PARAM_COUNT,
  LINT IN1,
  LINT IN2,
  PROGRAM0 *data__)
{
  LINT __res;
  BOOL __TMP_ENO = __GET_VAR(data__->ADD11_ENO,);
  __res = ADD__LINT__LINT(EN,
    &__TMP_ENO,
    __PARAM_COUNT,
    IN1,
    IN2);
  __SET_VAR(,data__->ADD11_ENO,,__TMP_ENO);
  return __res;
}

void PROGRAM0_init__(PROGRAM0 *data__, BOOL retain) {
  __INIT_VAR(data__->SWITCH,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->COUNTER,0,retain)
  __INIT_VAR(data__->ONE,1,retain)
  __INIT_VAR(data__->SPEED,1,retain)
  __INIT_VAR(data__->TARGET1,__STRING_LITERAL(42,"219.91,-332.00,289.34,0.21,0.66,-0.65,0.32"),retain)
  __INIT_VAR(data__->TARGET2,__STRING_LITERAL(42,"636.63,138.27,410.64,0.12,-0.72,0.07,-0.68"),retain)
  R_TRIG_init__(&data__->R_TRIG0,retain);
  MOVEARM_init__(&data__->FUNCTIONBLOCK1,retain);
  MOVEARM_init__(&data__->FUNCTIONBLOCK0,retain);
  R_TRIG_init__(&data__->R_TRIG1,retain);
  __INIT_VAR(data__->OR8_OUT,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->ADD11_ENO,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->ADD11_OUT,0,retain)
}

// Code part
void PROGRAM0_body__(PROGRAM0 *data__) {
  // Initialise TEMP variables

  __SET_VAR(data__->FUNCTIONBLOCK1.,ENABLE,,__GET_VAR(data__->FUNCTIONBLOCK0.VALID,));
  __SET_VAR(data__->FUNCTIONBLOCK1.,SPEED,,__GET_VAR(data__->SPEED,));
  __SET_VAR(data__->FUNCTIONBLOCK1.,TARGET,,__GET_VAR(data__->TARGET2,));
  MOVEARM_body__(&data__->FUNCTIONBLOCK1);
  __SET_VAR(data__->R_TRIG0.,CLK,,__GET_VAR(data__->SWITCH,));
  R_TRIG_body__(&data__->R_TRIG0);
  __SET_VAR(data__->,OR8_OUT,,OR__BOOL__BOOL(
    (BOOL)__BOOL_LITERAL(TRUE),
    NULL,
    (UINT)2,
    (BOOL)__GET_VAR(data__->FUNCTIONBLOCK1.VALID,),
    (BOOL)__GET_VAR(data__->R_TRIG0.Q,)));
  __SET_VAR(data__->FUNCTIONBLOCK0.,ENABLE,,__GET_VAR(data__->OR8_OUT,));
  __SET_VAR(data__->FUNCTIONBLOCK0.,SPEED,,__GET_VAR(data__->SPEED,));
  __SET_VAR(data__->FUNCTIONBLOCK0.,TARGET,,__GET_VAR(data__->TARGET1,));
  MOVEARM_body__(&data__->FUNCTIONBLOCK0);
  __SET_VAR(data__->R_TRIG1.,CLK,,(__GET_VAR(data__->FUNCTIONBLOCK0.VALID,) || __GET_VAR(data__->FUNCTIONBLOCK1.VALID,)));
  R_TRIG_body__(&data__->R_TRIG1);
  __SET_VAR(data__->,ADD11_OUT,,__PROGRAM0_ADD__LINT__LINT1(
    (BOOL)__GET_VAR(data__->R_TRIG1.Q,),
    (UINT)2,
    (LINT)__GET_VAR(data__->ONE,),
    (LINT)__GET_VAR(data__->COUNTER,),
    data__));
  if (__GET_VAR(data__->ADD11_ENO,)) {
    __SET_VAR(data__->,COUNTER,,__GET_VAR(data__->ADD11_OUT,));
  };

  goto __end;

__end:
  return;
} // PROGRAM0_body__() 





