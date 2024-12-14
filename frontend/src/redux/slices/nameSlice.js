import { createSlice } from "@reduxjs/toolkit";

const nameSlice = createSlice({
  name: "name",
  initialState: {
    check: [
      {
        download: false,
        name: "",
      },
      {
        download: false,
        name: "",
      },
      {
        download: false,
        name: "",
      },
      {
        download: false,
        name: "",
      },
    ],
    statement: [
      {
        download: false,
        name: "",
      },
      {
        download: false,
        name: "",
      },
      {
        download: false,
        name: "",
      },
      {
        download: false,
        name: "",
      },
    ],
  },
  reducers: {
    setCheck: (state, action) => {
      state.check[action.payload.index] = {
        download: action.payload.download,
        name: action.payload.name,
      };
    },
    setStatement: (state, action) => {
      state.statement[action.payload.index] = {
        download: action.payload.download,
        name: action.payload.name,
      };
    },
    initCheckStatement: (state, action) => {
      state.check[action.payload] = {
        download: false,
        name: "",
      };
      state.statement[action.payload] = {
        download: false,
        name: "",
      };
    },
  },
});

export const { setCheck, setStatement, initCheckStatement } = nameSlice.actions;
export default nameSlice.reducer;
