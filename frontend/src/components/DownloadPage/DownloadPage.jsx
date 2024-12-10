import { downloadFile } from "../../redux/slices/fileSlice";
import BorderButton from "../BorderButton/BorderButton";
import { useSelector, useDispatch } from "react-redux";
import classes from "./DownloadPage.module.css";
import jackdaw from "../../assets/jackdaw.png";
import { useEffect, useState } from "react";

const DownloadPage = () => {
  const dispatch = useDispatch();
  const { downloadData, downloadStatus, downloadError } = useSelector(
    (state) => state.file
  );
  const [isRight, setIsRight] = useState(false);

  const handleDownload = () => {
    if (isRight) {
      dispatch(downloadFile("12"));
    }
  };

  useEffect(() => {
    if (downloadData) {
      console.log("download");
      const url = window.URL.createObjectURL(new Blob([downloadData]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "document.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();
    }
  }, [downloadData]);

  return (
    <div className={classes.wrapper}>
      <div className={classes.title}>
        <p>Результаты проверки</p>
      </div>

      <div className={classes.card}>
        <div className={classes.controller}>
          <div className={classes.rightBlock}>
            <div
              className={classes.checkBox}
              style={{ backgroundColor: isRight ? "#148F2B" : "#FFFFFF" }}
              onClick={() => setIsRight(!isRight)}
            >
              <img
                src={jackdaw}
                alt=""
                style={{ display: isRight ? "block" : "none" }}
              />
            </div>
            <p>Согласие на удаление персональных данных</p>
          </div>

          <div
            className={classes.btn}
            onClick={handleDownload}
            style={{ opacity: isRight ? "1" : ".5" }}
          >
            <p>Скачать</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DownloadPage;
