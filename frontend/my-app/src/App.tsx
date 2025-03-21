import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import MockSearchPageV2 from "./routes/mock-v2";
import SearchMockV2 from "./routes/SearchMockV2";
import SearchV2 from "./routes/SearchV2";
import { ColorModeSwitcher } from "./ColorModeSwitcher";
import Landing from "./routes/Landing";

export default function App() {
  return (
    <Router>
      <ColorModeSwitcher />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/mock/search" element={<SearchMockV2 />} />
        <Route path="/v2/search" element={<SearchV2 />} />
      </Routes>
    </Router>
  );
}
