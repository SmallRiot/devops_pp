import classes from "./RadioButtons.module.css";
import { useSelector, useDispatch } from "react-redux";
import { selectOption } from "../../redux/slices/radioSlice";

const RadioButtons = ({ index }) => {
  const dispatch = useDispatch();
  const selected = useSelector((state) => state.radio.selectedOption);
  const freezes = useSelector((state) => state.radio.freeze);
  console.log("Selected: " + selected[index]);
  return (
    <div className={classes.block}>
      <div className={classes.radioBtn}>
        <p>Наличными</p>
        <div
          className={classes.dot}
          onClick={() => {
            if (!freezes[index]) {
              dispatch(selectOption({ select: "cash", index }));
            }
          }}
        >
          <span
            className={`${classes.down} ${
              selected[index] === "cash" ? classes.downActive : ""
            }`}
          ></span>
          <span
            className={`${classes.up} ${
              selected[index] === "cash" ? classes.upActive : ""
            }`}
          ></span>
        </div>
      </div>
      <div className={classes.radioBtn}>
        <p>Безналичный расчет</p>
        <div
          className={classes.dot}
          onClick={() => {
            if (!freezes[index]) {
              dispatch(selectOption({ select: "nonCash", index }));
            }
          }}
        >
          <span
            className={`${classes.down} ${
              selected[index] === "nonCash" ? classes.downActive : ""
            }`}
          ></span>
          <span
            className={`${classes.up} ${
              selected[index] === "nonCash" ? classes.upActive : ""
            }`}
          ></span>
        </div>
      </div>
    </div>
  );
};

export default RadioButtons;
