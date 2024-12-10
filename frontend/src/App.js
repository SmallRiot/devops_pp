import "./App.css";
import Header from "./components/Header/Header";
import Start from "./components/Start/Start";
import BankPage from "./components/BankPage/BankPage";
import { Route, Routes } from "react-router-dom";
import Card from "./components/Card/Card";
import PaymentCard from "./components/PaymentCard/PaymentCard";
import { useSelector } from "react-redux";
import DownloadPage from "./components/DownloadPage/DownloadPage";

function App() {
  const arr = useSelector((state) => state.docs.routes);
  console.log("APP render");
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="" element={<Start />} />
        <Route path="/bank" element={<BankPage />}>
          {arr.map((el) => {
            if (el.initPath !== "/bank/checks") {
              return <Route path={el.initPath} element={<Card obj={el} />} />;
            } else {
              return (
                <Route path={el.initPath} element={<PaymentCard obj={el} />} />
              );
            }
          })}
        </Route>
        <Route path="/document" element={<DownloadPage />} />
      </Routes>
    </div>
  );
}

export default App;
