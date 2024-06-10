import "./App.css";
import AddressSearchBox from "./components/AddressSearchBox";

function App() {
  return (
    <div className="flex flex-col items-center w-full min-h-screen bg-gradient-to-r from-sky-100/70 to-pink-200/40">
      <div className="w-full max-w-4xl p-6">
        <h1 className="mt-8 mb-8 text-sky-900 text-center font-semibold">
          Search your home address here
        </h1>
        <AddressSearchBox />
      </div>
    </div>
  );
}

export default App;
