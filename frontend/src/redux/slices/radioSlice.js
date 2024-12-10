import { createSlice } from "@reduxjs/toolkit";

const radioSlice = createSlice({
  name: "radio",
  initialState: {
    selectedOption: [""],
    freeze: [false],
  },
  reducers: {
    selectOption: (state, action) => {
      if (
        state.selectedOption[action.payload.index] !== action.payload.select
      ) {
        state.selectedOption[action.payload.index] = action.payload.select;
      }
    },
    setFreeze: (state, action) => {
      state.freeze[action.payload.index] = action.payload.freeze;
    },
  },
});

export const { selectOption, setFreeze } = radioSlice.actions;
export default radioSlice.reducer;
