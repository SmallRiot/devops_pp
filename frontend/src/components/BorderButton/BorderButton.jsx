import { Link } from "react-router-dom";
import classes from "./BorderButton.module.css";

const BorderButton = ({ style, path, onClick }) => {
  return (
    <Link to={path} className={classes.btn} style={style}>
      <div className={classes.content} onClick={onClick}>
        <p>Далее</p>
        <p>→</p>
      </div>
    </Link>
  );
};

export default BorderButton;
