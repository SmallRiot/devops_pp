import image from "../../assets/image.png";
import classes from "./Start.module.css";
import SelectBlock from "../SelectBlock/SelectBlock";
import { useEffect } from "react";
import { v4 as uuidv4 } from "uuid";

const Start = () => {
  useEffect(() => {
    const newSessionId = uuidv4();
    // sessionStorage.setItem("sessionId", newSessionId);
    document.cookie = `mainSessionId=${newSessionId}; path=/; max-age=3600`;
    console.log("mainSessionId: " + newSessionId);
  }, []);

  return (
    <div className={classes.start}>
      <div className={classes.wrapper}>
        <div className={classes.text}>
          <p className={classes.title}>
            Платформа автоматизированной проверки документов на материальную
            помощь{" "}
          </p>
          <ul>
            <li>Загружайте необходимые документы</li>
            <li>
              Скачивайте автоматически сгенерированный проверенный документ
            </li>
          </ul>
        </div>
        <div>
          <img src={image} alt="" />
        </div>
      </div>
      <SelectBlock />
    </div>
  );
};

export default Start;
