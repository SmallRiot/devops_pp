import { Outlet } from "react-router-dom";
import Subsequence from "../Subsequence/Subsequence";
import classes from "./BankPage.module.css";
import { useSelector } from "react-redux";

const BankPage = () => {
  const title = useSelector((state) => state.title.title);
  return (
    <div>
      <div className={classes.wrapper}>
        <div className={classes.title}>
          <p>{title}</p>
        </div>
        <Subsequence />
      </div>
      <Outlet />
    </div>
  );
};

export default BankPage;
