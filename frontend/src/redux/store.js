import { configureStore } from "@reduxjs/toolkit";
import radioReducer from "../redux/slices/radioSlice";
import routesReducer from "../redux/slices/routesSlice";
import fileReducer from "../redux/slices/fileSlice";
import titleReducer from "../redux/slices/titleSlice";
import nameReducer from "../redux/slices/nameSlice";
import componentsCheckSlice from "../redux/slices/componentsCheckSlice";

const store = configureStore({
  reducer: {
    radio: radioReducer,
    routes: routesReducer,
    file: fileReducer,
    title: titleReducer,
    name: nameReducer,
    components: componentsCheckSlice,
  },
});

export default store;
