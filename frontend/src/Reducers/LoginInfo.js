import React, {useReducer} from 'react';
export const loginInitialState = {
  login: false
}

export const loginReducer = (state, action) => {
  switch (action.type){
    case 'login':
      return {login: true};
    case 'logout':
      return {login: false};
    default:
      throw new Error();
  }
}
