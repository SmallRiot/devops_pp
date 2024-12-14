import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

export const loadComponentsFromLocalStorage = createAsyncThunk(
  "components/localComponentsFromLocalStorage",
  async () => {
    const savedComponents = localStorage.getItem("components");
    return savedComponents ? JSON.parse(savedComponents) : [];
  }
);

export const saveComponentsFromLocalStorage = createAsyncThunk(
  "components/saveComponentsFromLocalStorage",
  async (components) => {
    localStorage.setItem("components", JSON.stringify(components));
    return components;
  }
);

const componentsCheckSlice = createSlice({
  name: "components",
  initialState: {
    components: [
      {
        id: 0,
        freeze: false,
        nameCheck: "",
        nameStatement: "",
        downloadCheck: false,
        downloadStatement: false,
        paymentType: "",
      },
    ],
    foundComponent: "",
  },
  reducers: {
    addComponent: (state) => {
      state.components.push({
        id: state.components.length,
        freeze: false,
        nameCheck: "",
        nameStatement: "",
        downloadCheck: false,
        downloadStatement: false,
        paymentType: "",
      });
    },
    findComponent: (state, action) => {
      const i = state.components.findIndex(
        (component) => component.id === action.payload
      );
      if (i !== -1) {
        state.foundComponent = state.components[i];
      }
      // state.foundComponent = state.components.find(
      //   (component) => component.id === action.payload
      // );
    },
    updatePaymentType: (state, action) => {
      const { index, paymentType } = action.payload;
      const i = state.components.findIndex(
        (component) => component.id === index
      );
      if (i !== -1) {
        state.components[i].paymentType = paymentType;
        state.foundComponent = state.components[i];
      }
    },
    updateCheck: (state, action) => {
      const { index, name, download } = action.payload;
      const i = state.components.findIndex(
        (component) => component.id === index
      );
      if (i !== -1) {
        state.components[i].nameCheck = name;
        state.components[i].downloadCheck = download;
        state.foundComponent = state.components[i];
      }
    },
    updateStatement: (state, action) => {
      const { index, name, download } = action.payload;
      const i = state.components.findIndex(
        (component) => component.id === index
      );
      if (i !== -1) {
        state.components[i].nameStatement = name;
        state.components[i].downloadStatement = download;
        state.foundComponent = state.components[i];
      }
    },
    updateFreeze: (state, action) => {
      const { index, freeze } = action.payload;
      const i = state.components.findIndex(
        (component) => component.id === index
      );
      if (i !== -1) {
        state.components[i].freeze = freeze;
        state.foundComponent = state.components[i];
      }
    },
  },
});

export const {
  addComponent,
  findComponent,
  updatePaymentType,
  updateCheck,
  updateFreeze,
  updateStatement,
} = componentsCheckSlice.actions;
export default componentsCheckSlice.reducer;
