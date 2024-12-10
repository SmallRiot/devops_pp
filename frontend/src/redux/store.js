import { configureStore } from "@reduxjs/toolkit";
import radioReducer from "../redux/slices/radioSlice";
import docsReducer from "../redux/slices/docsSlice";
import fileReducer from "../redux/slices/fileSlice";
import titleReducer from "../redux/slices/titleSlice";
import nameReducer from "../redux/slices/nameSlice";

const store = configureStore({
  reducer: {
    radio: radioReducer,
    docs: docsReducer,
    file: fileReducer,
    title: titleReducer,
    name: nameReducer,
  },
});

export default store;
