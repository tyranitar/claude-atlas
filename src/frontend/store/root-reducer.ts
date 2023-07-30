import { reducers as apiReducers } from "./services";
// import * as sliceReducers from "./slices";
import { combineReducers } from "redux";

export const rootReducer = combineReducers({
  //   ...sliceReducers,
  ...apiReducers,
});

export type RootState = ReturnType<typeof rootReducer>;
