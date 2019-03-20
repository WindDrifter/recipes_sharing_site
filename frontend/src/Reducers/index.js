
import { LOGIN, LOGOUT } from "../constants/action-constants";


const initialState = {
  login: false
};
function rootReducer(state = initialState, action) {
  switch (action.type){
    case LOGIN:
      return {login: true};
    case LOGOUT:
      return {login: false};
    default:
      return state;
  }
};
export default rootReducer;
