import classes from "./SubmitButton.module.css";

const SubmitButton = ({ className = "" }) => {
  return (
    <div className={`${classes.btn} ${className}`}>
      <div>
        <p>Подать документы</p>
        <p className={classes.arrow}>→</p>
      </div>
    </div>
  );
};

export default SubmitButton;
