// import logo from './logo.svg';
import './App.css';
import Result from './result'
import File from './file'
import CurrentFiles from './currentFiles'
import Form from './form'

function App() {
  return (
    <div className="App">
      <header>
        Search Engine - CS 222
      </header>
      <div className = "grid grid-cols-2 gap-4">
        <div>
          <Result /> 
        </div>
        <div className='grid grid-flow-row auto-rows-max'>
          <div className='grid grid-cols-2 gap-2'>
            <div><File /></div>
            <div>
              <CurrentFiles />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
