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
  },
});

export const { setCheck, setStatement } = nameSlice.actions;
export default nameSlice.reducer;
