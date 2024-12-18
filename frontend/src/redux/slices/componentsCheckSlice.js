import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";

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

const apiUrl = process.env.REACT_APP_API_URL;

export const uploadBankFile = createAsyncThunk(
  "bank/uploadFile",
  async ({ file, id }, { rejectWithValue }) => {
    const formData = new FormData();
    formData.append("path", file);
    try {
      const response = await axios.post(`${apiUrl}/api/documents/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true,
      });

      return response.data;
    } catch (error) {
      console.log("Error to response: " + JSON.stringify(error));
      if (error.status === 500) {
        return rejectWithValue("Внутренняя ошибка сервера");
      }
      return error.response
        ? rejectWithValue(error.response.data)
        : rejectWithValue("Отсутствует соединение с сервером");
    }
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
        uploadCheckStatus: "idle",
        uploadCheckError: null,
        uploadStatementStatus: "idle",
        uploadStatementError: null,
      },
    ],
    foundComponent: "",
  },
  reducers: {
    addComponent: (state) => {
      // state.components.push({
      //   id: state.components.length,
      //   freeze: false,
      //   nameCheck: "",
      //   nameStatement: "",
      //   downloadCheck: false,
      //   downloadStatement: false,
      //   paymentType: "",
      // });
      state.components = [
        ...state.components,
        {
          id: state.components.length,
          freeze: false,
          nameCheck: "",
          nameStatement: "",
          downloadCheck: false,
          downloadStatement: false,
          paymentType: "",
          uploadCheckStatus: "idle",
          uploadCheckError: null,
          uploadStatementStatus: "idle",
          uploadStatementError: null,
        },
      ];
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
  extraReducers: (builder) => {
    builder
      .addCase(uploadBankFile.pending, (state, action) => {
        console.log("Name: " + action.meta.arg.file.name);
        const i = action.meta.arg.id;
        if (action.meta.arg.file.name.includes("cheque")) {
          state.components[i].uploadCheckStatus = "loading";
          state.components[i].uploadCheckError = null;
        } else {
          state.components[i].uploadStatementStatus = "loading";
          state.components[i].uploadStatementError = null;
        }
      })
      .addCase(uploadBankFile.fulfilled, (state, action) => {
        const i = action.meta.arg.id;
        if (action.meta.arg.file.name.includes("cheque")) {
          state.components[i].uploadCheckStatus = "succeeded";
        } else {
          state.components[i].uploadStatementStatus = "succeeded";
        }
      })
      .addCase(uploadBankFile.rejected, (state, action) => {
        console.log("Failed: " + JSON.stringify(action.payload));
        const i = action.meta.arg.id;
        if (action.meta.arg.file.name.includes("cheque")) {
          state.components[i].uploadCheckStatus = "failed";
          state.components[i].uploadCheckError =
            typeof action.payload === "string"
              ? action.payload
              : action.payload?.message || "Внутренняя ошибка сервера";
        } else {
          state.components[i].uploadStatementStatus = "failed";
          state.components[i].uploadStatementError =
            typeof action.payload === "string"
              ? action.payload
              : action.payload?.message || "Внутренняя ошибка сервера";
        }
      });
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
