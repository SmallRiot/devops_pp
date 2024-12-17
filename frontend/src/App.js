import "./App.css";
import Header from "./components/Header/Header";
import Start from "./components/Start/Start";
import BankPage from "./components/BankPage/BankPage";
import { Route, Routes } from "react-router-dom";
import Card from "./components/Card/Card";
import PaymentCard from "./components/PaymentCard/PaymentCard";
import { useDispatch, useSelector } from "react-redux";
import DownloadPage from "./components/DownloadPage/DownloadPage";
import { useEffect } from "react";
import { loadRoutesFromLocalStorage } from "./redux/slices/routesSlice";
import NotFoundPage from "./components/NotFoundPage/NotFoundPage";

function App() {
  const dispatch = useDispatch();
  const routes = useSelector((state) => state.routes.routes);
  useEffect(() => {
    dispatch(loadRoutesFromLocalStorage());
  }, [dispatch]);

  console.log("APP render");

  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="" element={<Start />} />
        <Route path="/bank" element={<BankPage />}>
          {routes.map((el) => {
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
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </div>
  );
}

export default App;
