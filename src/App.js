import Main from "./pages/main/Main";
import InputMeme from "./pages/input/InputMeme";
import Result from "./pages/result/result";
import "./reset.css";
import "./App.css";
import { Route } from "react-router-dom";
import Select from "./pages/select/Select";

<style>#sev_hhtml{}</style>;

function App() {
  return (
    <div className="App">
      <Route path="/" component={Main} exact sensitive="false" />
      <Route path="/input-meme" component={InputMeme} />
      <Route path="/select/:name" component={Select} />
      <Route path="/result" component={Result} />
    </div>
  );
}

export default App;
