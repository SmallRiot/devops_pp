import { useDispatch, useSelector } from "react-redux";
import DownloadButton from "../DownloadButton/DownloadButton";
import RadioButtons from "../RadioButtons/RadioButtons";
import classes from "./CheckController.module.css";
import BorderButton from "../BorderButton/BorderButton";
import { useRef, useState } from "react";
import { renameFileCheck, renameFileStatement } from "../../utils/converter";
import { uploadFile } from "../../redux/slices/fileSlice";
import { setCheck, setStatement } from "../../redux/slices/nameSlice";
import success from "../../assets/success.png";
import errorImg from "../../assets/errorImg.png";
import { setFreeze } from "../../redux/slices/radioSlice";
import { TailSpin } from "react-loader-spinner";

const CheckController = ({ title, index }) => {
  const dispatch = useDispatch();
  const selected = useSelector((state) => state.radio.selectedOption);
  const check = useSelector((state) => state.name.check);
  const statement = useSelector((state) => state.name.statement);
  const { uploadStatus, uploadError } = useSelector((state) => state.file);
  const checkInputRef = useRef(null);
  const statementInputRef = useRef(null);
  const choice = useRef("");

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      let newFile;
      if (choice.current === "check") {
        newFile = renameFileCheck(file, index);
        dispatch(setCheck({ download: true, name: file.name, index: index }));
      } else {
        newFile = renameFileStatement(file, index);
        dispatch(
          setStatement({ download: true, name: file.name, index: index })
        );
      }

      dispatch(uploadFile(newFile));
      dispatch(setFreeze({ freeze: true, index: index }));
    }
  };

  const handleUploadCheckClick = () => {
    choice.current = "check";
    checkInputRef.current.click();
  };

  const handleUploadStatementClick = () => {
    choice.current = "statement";
    statementInputRef.current.click();
  };

  return (
    <div className={classes.paymentBlock}>
      <p className={classes.question}>Как производилась оплата?</p>
      <RadioButtons index={index} />
      {selected[index] === "cash" && (
        <div style={{ display: "flex" }}>
          <input
            type="file"
            onChange={handleFileChange}
            style={{ display: "none" }}
            ref={checkInputRef}
          />
          {!check[index].download && (
            <DownloadButton
              onClick={handleUploadCheckClick}
              text={"Загрузите чек"}
              style={{ padding: "10px 45px", fontSize: "20px" }}
            />
          )}
          {uploadStatus === "succeeded" && check[index].download && (
            <div className={classes.requestBlock}>
              <img src={success} />
              <p>{check[index].name}</p>
            </div>
          )}
          {/* {uploadStatus === "loading" && (
            <div className={classes.requestBlock}>
              <TailSpin color="#148F2B" height={55} width={55} />
            </div>
          )} */}
          {uploadStatus === "failed" && (
            <div className={classes.requestBlock}>
              <img src={errorImg} />
              <p>{uploadError.message || uploadError}</p>
            </div>
          )}
        </div>
      )}
      {selected[index] === "nonCash" && (
        <div className={classes.btn}>
          <input
            type="file"
            onChange={handleFileChange}
            style={{ display: "none" }}
            ref={checkInputRef}
          />
          {!check[index].download && (
            <DownloadButton
              onClick={handleUploadCheckClick}
              text={"Загрузите чек"}
              style={{
                padding: "10px 45px",
                fontSize: "20px",
              }}
              freeze={!statement[index].download}
            />
          )}
          {uploadStatus === "succeeded" && check[index].download && (
            <div className={classes.requestBlock}>
              <img src={success} />
              <p>{check[index].name}</p>
            </div>
          )}
          {/* {uploadStatus === "loading" && !check[index].download && (
            <div className={classes.requestBlock}>
              <TailSpin color="#148F2B" height={55} width={55} />
            </div>
          )} */}
          <input
            type="file"
            onChange={handleFileChange}
            style={{ display: "none" }}
            ref={statementInputRef}
          />
          {!statement[index].download && (
            <DownloadButton
              onClick={handleUploadStatementClick}
              text={"Загрузите выписку"}
              style={{ padding: "10px 45px", fontSize: "20px" }}
            />
          )}
          {uploadStatus === "succeeded" && statement[index].download && (
            <div className={classes.requestBlock}>
              <img src={success} />
              <p>{statement[index].name}</p>
            </div>
          )}
          {/* {uploadStatus === "loading" && (
              <div className={classes.requestBlock}>
                <TailSpin color="#148F2B" height={55} width={55} />
              </div>
            )} */}
        </div>
      )}
    </div>
  );
};

export default CheckController;
