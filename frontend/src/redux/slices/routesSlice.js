import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

export const loadRoutesFromLocalStorage = createAsyncThunk(
  "routes/localRoutesFromLocalStorage",
  async () => {
    const savedRoutes = localStorage.getItem("routes");
    return savedRoutes ? JSON.parse(savedRoutes) : [];
  }
);

export const saveRoutesFromLocalStorage = createAsyncThunk(
  "routes/saveRoutesFromLocalStorage",
  async (routes) => {
    localStorage.setItem("routes", JSON.stringify(routes));
    return routes;
  }
);

const routesSlice = createSlice({
  name: "routes",
  initialState: {
    routes: [],
  },
  reducers: {
    setRouts: (state, action) => {
      state.routes = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadRoutesFromLocalStorage.fulfilled, (state, action) => {
        // state.status = "succeeded";
        state.routes = action.payload;
      })
      .addCase(saveRoutesFromLocalStorage.fulfilled, (state, action) => {
        // state.status = "succeeded";
        state.routes = action.payload;
      });
    // .addCase(loadRoutesFromLocalStorage.rejected, (state, action) => {
    //   state.status = "failed";
    //   state.error = action.error.message;
    // })
    // .addCase(saveComponentsToLocalStorage.fulfilled, (state, action) => {
    //   state.items = action.payload;
    // });
  },
});

export const getPathIndexByName = (state, pathName) =>
  state.routes.findIndex((el) => {
    let arr = el.initPath.split("/");
    return arr[arr.length - 1] === pathName;
  });

export const { setRouts } = routesSlice.actions;
export default routesSlice.reducer;
