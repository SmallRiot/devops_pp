// src/features/fileSlice.js
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const uploadFile = createAsyncThunk(
  "file/uploadFile",
  async (file, { rejectWithValue }) => {
    const formData = new FormData();
    formData.append("path", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/documents/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          withCredentials: true,
        }
      );

      return response.data;
    } catch (error) {
      return error.response
        ? rejectWithValue(error.response.data.path)
        : rejectWithValue("Отсутствует соединение с сервером");
    }
  }
);

export const downloadFile = createAsyncThunk(
  "file/downloadFile",
  async (id, { rejectWithValue }) => {
    try {
      console.log("request");
      const response = await axios.get(
        "http://127.0.0.1:8000/api/api/combine_pdf",
        {
          responseType: "blob",
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true,
        }
      );
      console.log(response.data.path);
      return response.data;
    } catch (error) {
      const headers = {};
      error.response.headers.forEach((value, key) => {
        headers[key] = value;
      });
      console.log("Error: " + error.message);
      return error.response
        ? rejectWithValue({ errorMessage: error.message })
        : rejectWithValue("Отсутствует соединение с сервером");
    }
  }
);

const fileSlice = createSlice({
  name: "file",
  initialState: {
    uploadStatus: "idle", // 'idle' | 'loading' | 'succeeded' | 'failed'
    downloadStatus: "idle",
    uploadError: null,
    downloadError: null,
    downloadData: null,
  },
  reducers: {
    initUploadFile: (state, action) => {
      state.uploadStatus = "idle";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(uploadFile.pending, (state) => {
        state.uploadStatus = "loading";
        state.uploadError = null;
      })
      .addCase(uploadFile.fulfilled, (state) => {
        state.uploadStatus = "succeeded";
      })
      .addCase(uploadFile.rejected, (state, action) => {
        state.uploadStatus = "failed";
        state.uploadError = action.payload;
      })
      .addCase(downloadFile.pending, (state) => {
        state.downloadStatus = "loading";
        state.uploadError = null;
      })
      .addCase(downloadFile.fulfilled, (state, action) => {
        state.downloadStatus = "succeeded";
        state.downloadData = action.payload;
      })
      .addCase(downloadFile.rejected, (state, action) => {
        state.downloadStatus = "failed";
        state.downloadError = action.payload;
      });
  },
});

export default fileSlice.reducer;
export const { initUploadFile } = fileSlice.actions;
