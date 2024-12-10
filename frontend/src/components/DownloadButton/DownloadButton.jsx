import classes from "./DownloadButton.module.css";

const DownloadButton = ({ style, text, onClick, freeze = false }) => {
  return (
    <div
      onClick={() => {
        if (!freeze) {
          onClick();
        }
      }}
      className={`${classes.btn} ${freeze ? classes.btnDisable : ""}`}
      style={style}
    >
      <p>{text}</p>
    </div>
  );
};

export default DownloadButton;
