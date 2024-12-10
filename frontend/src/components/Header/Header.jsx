import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";
import classes from "./Header.module.css";

const Header = () => {
  return (
    <div className={classes.wrapper}>
      <Link to="">
        <div className={classes.block}>
          <div>
            <img src={logo} alt="" />
          </div>
          <div>
            <p>AutoVerify</p>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default Header;
