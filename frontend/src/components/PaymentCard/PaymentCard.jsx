import { useDispatch, useSelector } from "react-redux";
import DownloadButton from "../DownloadButton/DownloadButton";
import RadioButtons from "../RadioButtons/RadioButtons";
import classes from "./PaymentCard.module.css";
import BorderButton from "../BorderButton/BorderButton";
import { useEffect, useRef, useState } from "react";
import { renameFile, renameFileStatement } from "../../utils/converter";
import { initUploadFile, uploadFile } from "../../redux/slices/fileSlice";
import { addComponent } from "../../redux/slices/componentsCheckSlice";
import {
  initCheckStatement,
  setCheck,
  setStatement,
} from "../../redux/slices/nameSlice";
import success from "../../assets/success.png";
import { setFreeze } from "../../redux/slices/radioSlice";
import { TailSpin } from "react-loader-spinner";
import CheckController from "../CheckController/CheckController";
import MoreButton from "../MoreButton/MoreButton";

const PaymentCard = ({ obj }) => {
  const dispatch = useDispatch();
  //
  // Достаем из локального хранилища компоненты
  //
  // const selected = useSelector((state) => state.radio.selectedOption);
  const components = useSelector((state) => state.components.components);
  // const check = useSelector((state) => state.name.check);
  // const statement = useSelector((state) => state.name.statement);
  const { uploadStatus, uploadError } = useSelector((state) => state.file);
  // const checkInputRef = useRef(null);
  // const statementInputRef = useRef(null);
  // const choice = useRef("");
  // const [nameCheck, setNameCheck] = useState("");
  // const [nameStatement, setNameStatement] = useState("");
  // const [components, setComponents] = useState([{ id: 0 }]);
  // const [render, setRender] = useState("");

  const handleClickMore = () => {
    // setComponents((prevData) => [...prevData, { id: prevData.length }]);
    // dispatch(addComponent());
  };

  const handleUpload = () => {
    // if (isRight || uploadStatus === "succeeded") {
    dispatch(initUploadFile());
    // }
  };

  console.log("render PaymentCard " + JSON.stringify(components, null, 2));
  return (
    <div className={classes.wrapper}>
      <p className={classes.title}>{obj.title}</p>
      <p className={classes.subTitle}>{obj.subTitle}</p>
      <div className={classes.controller}>
        {components.map((el) => {
          console.log(
            "Component N" + el.id + "   " + JSON.stringify(el, null, 2)
          );
          return (
            <CheckController key={el.id} title={obj.title} index={el.id} />
          );
        })}
      </div>
      {/* {uploadStatus === "failed" && (
        <p
          onClick={() => {
            console.log("Id render: " + components[components.length - 1].id);
            dispatch(initUploadFile());
            dispatch(
              setFreeze({
                freeze: false,
                index: components[components.length - 1].id,
              })
            );
            dispatch(initCheckStatement(components.length - 1));
            setRender("123");
          }}
        >
          Загрузить ещё раз
        </p>
      )} */}
      <div className={classes.downBlock}>
        <MoreButton
          index={components.length - 1}
          onClick={() => dispatch(addComponent())}
        />
        <BorderButton
          onClick={handleUpload}
          path={obj.path}
          style={{ marginLeft: "auto", marginRight: "50px" }}
        />
      </div>
    </div>
  );
};

export default PaymentCard;
