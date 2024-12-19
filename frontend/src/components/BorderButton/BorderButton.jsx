import { Link, useNavigate } from "react-router-dom";
import classes from "./BorderButton.module.css";

const BorderButton = ({ style, path, onClick }) => {
  const navigate = useNavigate();

  const handleClick = async (event) => {
    event.preventDefault();
    await onClick();
    navigate(path);
  };

  return (
    <div className={classes.btn} style={style}>
      <div className={classes.content} onClick={handleClick}>
        <p>Далее</p>
        <p>→</p>
      </div>
    </div>
  );
};

export default BorderButton;
