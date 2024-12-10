import { useSelector } from "react-redux";
import classes from "./MoreButton.module.css";

const MoreButton = ({ style, onClick, index, show }) => {
  const selected = useSelector((state) => state.radio.selectedOption);
  const check = useSelector((state) => state.name.check);
  const statement = useSelector((state) => state.name.statement);
  const { uploadStatus, uploadError } = useSelector((state) => state.file);

  if (
    selected[index] === "cash" &&
    check[index].download &&
    uploadStatus === "succeeded"
  ) {
    show = true;
  }

  if (
    selected[index] === "nonCash" &&
    check[index].download &&
    statement[index].download &&
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
