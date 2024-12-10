import classes from "./Cell.module.css";

const Cell = ({ active = false, number = 1 }) => {
  return (
    <div className={`${classes.border} ${active ? classes.active : ""}`}>
      <div>
        <p
          style={{ color: active ? "#FFFFFF" : "#3B3636" }}
          className={classes.text}
        >
          {number}
        </p>
      </div>
    </div>
  );
};

export default Cell;
