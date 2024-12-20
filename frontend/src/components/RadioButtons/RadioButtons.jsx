import React, { useEffect } from "react";
import {
  findComponent,
  updatePaymentType,
} from "../../redux/slices/componentsCheckSlice";
import classes from "./RadioButtons.module.css";
import { useSelector, useDispatch } from "react-redux";

const RadioButtons = React.memo(({ component, index }) => {
  const dispatch = useDispatch();
  // const component = useSelector((state) => state.components.foundComponent);

  // useEffect(() => {
  //   dispatch(findComponent(index));
  // }, [dispatch, index]);
  // const selected = useSelector((state) => state.radio.selectedOption);
  // const freezes = useSelector((state) => state.radio.freeze);
  // console.log(
  //   "Selected: " +
  //     "with id " +
  //     index +
  //     "  " +
  //     JSON.stringify(component, null, 2)
  // );
  return (
    <div className={classes.block}>
      <div
        className={classes.radioBtn}
        onClick={() => {
          if (!component.freeze) {
            dispatch(updatePaymentType({ paymentType: "cash", index }));
          }
        }}
      >
        <p>Наличными</p>
        <div className={classes.dot}>
          <span
            className={`${classes.down} ${
              component.paymentType === "cash" ? classes.downActive : ""
            }`}
          ></span>
          <span
            className={`${classes.up} ${
              component.paymentType === "cash" ? classes.upActive : ""
            }`}
          ></span>
        </div>
      </div>
      <div
        className={classes.radioBtn}
        onClick={() => {
          if (!component.freeze) {
            dispatch(updatePaymentType({ paymentType: "nonCash", index }));
          }
        }}
      >
        <p>Безналичный расчет</p>
        <div className={classes.dot}>
          <span
            className={`${classes.down} ${
              component.paymentType === "nonCash" ? classes.downActive : ""
            }`}
          ></span>
          <span
            className={`${classes.up} ${
              component.paymentType === "nonCash" ? classes.upActive : ""
            }`}
          ></span>
        </div>
      </div>
    </div>
  );
});

export default RadioButtons;
