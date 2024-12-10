import { useLocation } from "react-router-dom";
import Cell from "../Cell/Cell";
import Separator from "../Separator/Separator";
import classes from "./Subsequence.module.css";
import { useSelector } from "react-redux";
import { getPathIndexByName } from "../../redux/slices/docsSlice";

const Subsequence = () => {
  const location = useLocation();
  const currentPath = location.pathname.slice(1);
  const arr = currentPath.split("/");
  const chapter = arr[arr.length - 1];
  console.log(chapter);
  const count = useSelector((state) => state.docs.routes.length);
  const index = useSelector((state) => getPathIndexByName(state.docs, chapter));
  let current = 0;
  console.log("Subsequence render");
  return (
    <div className={classes.block}>
      {Array(count * 2 - 1)
        .fill()
        .map((_, i) => {
          if (i % 2 === 0) {
            current += 1;
            return <Cell number={current} active={current - 1 === index} />;
          } else {
            return <Separator />;
          }
        })}
    </div>
  );
};

// {
//   Array(count)
//     .fill()
//     .map((_, i) => {
//       if (i + 1 === count) {
//         return <Cell number={i + 1} active={i === index} />;
//       } else {
//         return (
//           <div className={classes.cell}>
//             <Cell number={i + 1} active={i === index} />
//             <Separator />
//           </div>
//         );
//       }
//     });
// }

export default Subsequence;
