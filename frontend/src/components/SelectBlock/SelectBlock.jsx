import { Link } from "react-router-dom";
import SubmitButton from "../SubmitButton/SubmitButton";
import classes from "./SelectBlock.module.css";
import { useDispatch } from "react-redux";
import { setRouts } from "../../redux/slices/docsSlice";
import { all, franchise, medical, titles } from "../../mock/docs";
import { setTitle } from "../../redux/slices/titleSlice";

const SelectBlock = () => {
  const dispatch = useDispatch();

  return (
    <div className={classes.wrapper}>
      <div className={classes.block}>
        <p className={classes.title}>Компенсация денежных средств</p>
        <div className={classes.container}>
          <Link to="/bank/certificate">
            <div
              className={classes.item}
              onClick={() => {
                dispatch(setRouts(franchise));
                dispatch(setTitle(titles[0]));
              }}
            >
              <p className={classes.name}>
                Компенсация при оплате работником <span>Банка франшизы</span>
              </p>
              <SubmitButton className={classes.btn} />
            </div>
          </Link>
          <Link to="/bank/certificate">
            <div
              className={classes.item}
              onClick={() => {
                dispatch(setRouts(medical));
                dispatch(setTitle(titles[1]));
              }}
            >
              <p className={classes.name}>
                Компенсация при оплате <span>медицинских услуг</span>
              </p>
              <SubmitButton className={classes.btn} />
            </div>
          </Link>
          <Link to="/bank/certificate" className={classes.item3}>
            <div
              className={classes.item}
              onClick={() => {
                dispatch(setRouts(all));
                dispatch(setTitle(titles[2]));
              }}
            >
              <p className={classes.name}>
                Компенсация при оплате{" "}
                <span>медицинских услуг и Банка франшизы</span>
              </p>
              <SubmitButton className={classes.btn} />
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SelectBlock;
