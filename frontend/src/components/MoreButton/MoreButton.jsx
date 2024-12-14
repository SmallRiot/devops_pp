import { useDispatch, useSelector } from "react-redux";
import classes from "./MoreButton.module.css";
import { findComponent } from "../../redux/slices/componentsCheckSlice";
import { useEffect } from "react";

const MoreButton = ({ style, onClick, index, show }) => {
  const dispatch = useDispatch();
  const component = useSelector((state) => state.components.foundComponent);

  useEffect(() => {
    dispatch(findComponent(index));
  }, [dispatch, index]);

  const selected = useSelector((state) => state.radio.selectedOption);
  const check = useSelector((state) => state.name.check);
  const statement = useSelector((state) => state.name.statement);
  const { uploadStatus, uploadError } = useSelector((state) => state.file);

  if (
    component.paymentType === "cash" &&
    component.downloadCheck &&
    uploadStatus === "succeeded"
  ) {
    show = true;
  }

  if (
    component.paymentType === "nonCash" &&
    component.downloadCheck &&
    component.downloadStatement &&
    uploadStatus === "succeeded"
  ) {
    show = true;
  }

  return (
    <div
      onClick={() => {
        onClick();
        show = false;
      }}
      className={`${classes.btn} ${show ? "" : classes.btnDisable} ${
        index >= 3 ? classes.btnDisable : ""
      }`}
      style={style}
    >
      <p>Добавить ещё</p>
    </div>
  );
};

export default MoreButton;
