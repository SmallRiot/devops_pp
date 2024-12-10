import { useRef, useState } from "react";
import BorderButton from "../BorderButton/BorderButton";
import DownloadButton from "../DownloadButton/DownloadButton";
import { useSelector, useDispatch } from "react-redux";
import classes from "./Card.module.css";
import { uploadFile } from "../../redux/slices/fileSlice";
import success from "../../assets/success.png";
import errorImg from "../../assets/errorImg.png";
import jackdaw from "../../assets/jackdaw.png";
import { initUploadFile } from "../../redux/slices/fileSlice";
import { TailSpin } from "react-loader-spinner";
import { renameFile } from "../../utils/converter";

const Card = ({ obj }) => {
  const dispatch = useDispatch();
  const { uploadStatus, uploadError } = useSelector((state) => state.file);
  const [isRight, setIsRight] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const newFile = renameFile(file, obj.title);
      dispatch(uploadFile(newFile));
    }
  };
  const fileInputRef = useRef(null);
  const handleUploadClick = () => {
    fileInputRef.current.click();
  };
  const handleUpload = () => {
    // if (isRight || uploadStatus === "succeeded") {
    dispatch(initUploadFile());
    // }
  };
  console.log("Render Card");
  return (
    <div className={classes.wrapper}>
      <p className={classes.title}>{obj.title}</p>
      <p className={classes.subTitle}>{obj.subTitle}</p>
      <input
        type="file"
        onChange={handleFileChange}
        style={{ display: "none" }}
        ref={fileInputRef}
      />
      {uploadStatus === "idle" && (
        <DownloadButton
          onClick={handleUploadClick}
          style={{ alignSelf: "center" }}
          text={"Загрузить"}
        />
      )}
      {uploadStatus === "loading" && (
        <div className={classes.requestBlock}>
          <TailSpin color="#148F2B" height={100} width={100} />
        </div>
      )}
      {uploadStatus === "succeeded" && (
        <div className={classes.requestBlock}>
          <img src={success} />
        </div>
      )}
      {uploadStatus === "failed" && (
        <div className={classes.requestBlock}>
          <img src={errorImg} />
          <p>{uploadError.message || uploadError}</p>
        </div>
      )}
      <div className={classes.downBlock}>
        {uploadStatus === "failed" && (
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
            <p>Документ заполнен верно</p>
          </div>
        )}
        <BorderButton
          onClick={handleUpload}
          path={obj.path}
          style={{ marginLeft: "auto" }}
        />
      </div>
    </div>
  );
};

export default Card;
