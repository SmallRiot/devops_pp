import DownloadButton from "../DownloadButton/DownloadButton";
import classes from "./NotFoundPage.module.css";
import { Link } from "react-router-dom";

const NotFoundPage = () => {
  return (
    <div className={classes.wrapper}>
      <div className={classes.text}>
        <p>Все документы должны быть загружены в рамках одной сессии</p>
        <p>Перейдите на главную страницу, чтобы начать путь заново</p>
      </div>
      <Link to="">
        <DownloadButton text={"Перейти на главную страницу"} />
      </Link>
    </div>
  );
};

export default NotFoundPage;
