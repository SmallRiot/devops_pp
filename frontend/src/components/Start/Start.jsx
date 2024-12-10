import image from "../../assets/image.png";
import classes from "./Start.module.css";
import SelectBlock from "../SelectBlock/SelectBlock";

const Start = () => {
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
