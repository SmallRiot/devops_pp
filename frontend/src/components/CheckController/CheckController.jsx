import { createSelectorHook, useDispatch, useSelector } from "react-redux";
import DownloadButton from "../DownloadButton/DownloadButton";
import RadioButtons from "../RadioButtons/RadioButtons";
import classes from "./CheckController.module.css";
import BorderButton from "../BorderButton/BorderButton";
import React, { useEffect, useRef, useState } from "react";
import { renameFileCheck, renameFileStatement } from "../../utils/converter";
import { uploadFile } from "../../redux/slices/fileSlice";
import { setCheck, setStatement } from "../../redux/slices/nameSlice";
import success from "../../assets/success.png";
import errorImg from "../../assets/errorImg.png";
import { setFreeze } from "../../redux/slices/radioSlice";
import { TailSpin } from "react-loader-spinner";
import {
  findComponent,
  updateCheck,
  updateFreeze,
  updateStatement,
  uploadBankFile,
} from "../../redux/slices/componentsCheckSlice";

const CheckController = React.memo(({ component, index }) => {
  const dispatch = useDispatch();
  // const component = useSelector((state) => state.components.foundComponent);
  // const component = useSelector((state) => state.components.foundComponent);
  // const selected = useSelector((state) => state.radio.selectedOption);
  // const check = useSelector((state) => state.name.check);
  // const statement = useSelector((state) => state.name.statement);
  const { uploadCheckStatus, uploadCheckError, uploadStatus, uploadError } =
    useSelector((state) => state.file);
  const checkInputRef = useRef(null);
  const statementInputRef = useRef(null);
  const choice = useRef("");

  // useEffect(() => {
  //   dispatch(findComponent(index));
  // }, []);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      let newFile;
      if (choice.current === "check") {
        newFile = renameFileCheck(file, index);
        dispatch(
          updateCheck({ download: true, name: file.name, index: index })
        );
      } else {
        newFile = renameFileStatement(file, index);
        dispatch(
          updateStatement({ download: true, name: file.name, index: index })
        );
      }

      dispatch(uploadBankFile({ file: newFile, id: index }));
      dispatch(updateFreeze({ freeze: true, index: index }));
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
  console.log(
    "CheckController with id :" +
      index +
      "   " +
      JSON.stringify(component, null, 2)
  );
  return (
    <div className={classes.paymentBlock}>
      <p className={classes.question}>Как производилась оплата?</p>
      <RadioButtons component={component} index={index} />
      {component.paymentType === "cash" && (
        <div style={{ display: "flex" }}>
          <input
            type="file"
            onChange={handleFileChange}
            style={{ display: "none" }}
            ref={checkInputRef}
          />
          {!component.downloadCheck && (
            <DownloadButton
              onClick={handleUploadCheckClick}
              text={"Загрузите чек"}
              style={{ padding: "10px 45px", fontSize: "20px" }}
            />
          )}
          {component.uploadCheckStatus === "succeeded" &&
            component.downloadCheck && (
              <div className={classes.requestBlock}>
                <img src={success} />
                <p>{component.nameCheck}</p>
              </div>
            )}
          {component.uploadCheckStatus === "loading" && (
            <div className={classes.requestBlock}>
              <TailSpin color="#148F2B" height={55} width={55} />
            </div>
          )}
          {component.uploadCheckStatus === "failed" && (
            <div className={classes.requestBlock}>
              <img src={errorImg} />
              <p>{component.uploadCheckError}</p>
            </div>
          )}
        </div>
      )}
      {component.paymentType === "nonCash" && (
        <div className={classes.btn}>
          <input
            type="file"
            onChange={handleFileChange}
            style={{ display: "none" }}
            ref={checkInputRef}
          />
          {!component.downloadCheck && (
            <DownloadButton
              onClick={handleUploadCheckClick}
              text={"Загрузите чек"}
              style={{
                padding: "10px 45px",
                fontSize: "20px",
              }}
              freeze={!component.downloadStatement}
            />
          )}
          {component.uploadCheckStatus === "succeeded" &&
            component.downloadCheck && (
              <div className={classes.requestBlock}>
                <img src={success} />
                <p>{component.nameCheck}</p>
              </div>
            )}
          {component.uploadCheckStatus === "loading" && (
            <div className={classes.requestBlock}>
              <TailSpin color="#148F2B" height={55} width={55} />
            </div>
          )}
          {component.uploadCheckStatus === "failed" && (
            <div className={classes.requestBlock}>
              <img src={errorImg} />
              <p>{component.uploadCheckError}</p>
            </div>
          )}
          <input
            type="file"
            onChange={handleFileChange}
            style={{ display: "none" }}
            ref={statementInputRef}
          />
          {!component.downloadStatement && (
            <DownloadButton
              onClick={handleUploadStatementClick}
              text={"Загрузите выписку"}
              style={{ padding: "10px 45px", fontSize: "20px" }}
            />
          )}
          {component.uploadStatementStatus === "succeeded" &&
            component.downloadStatement && (
              <div className={classes.requestBlock}>
                <img src={success} />
                <p>{component.nameStatement}</p>
              </div>
            )}
          {component.uploadStatementStatus === "loading" && (
            <div className={classes.requestBlock}>
              <TailSpin color="#148F2B" height={55} width={55} />
            </div>
          )}
          {component.uploadStatementStatus === "failed" && (
            <div className={classes.requestBlock}>
              <img src={errorImg} />
              <p>{component.uploadStatementError}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
});

export default CheckController;
