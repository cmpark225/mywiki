# Local 개발 환경 설정

1. 프로젝트 생성 
```
# create-react-app 설치
npm install -g create-react-app

# 프로젝트 생성
create-react-app my-app
```

3. src 폴더 내 파일 삭제
```
cd my-app
rm -f src/*
removed 'src/App.css'
removed 'src/App.js'
removed 'src/App.test.js'
removed 'src/index.css'
removed 'src/index.js'
removed 'src/logo.svg'
removed 'src/registerServiceWorker.js'
```

4. src 폴더에 index.css 추가
src/index.css
```
body {
  font: 14px "Century Gothic", Futura, sans-serif;
  margin: 20px;
}

ol, ul {
  padding-left: 30px;
}

.board-row:after {
  clear: both;
  content: "";
  display: table;
}

.status {
  margin-bottom: 10px;
}

.square {
  background: #fff;
  border: 1px solid #999;
  float: left;
  font-size: 24px;
  font-weight: bold;
  line-height: 34px;
  height: 34px;
  margin-right: -1px;
  margin-top: -1px;
  padding: 0;
  text-align: center;
  width: 34px;
}

.square:focus {
  outline: none;
}

.kbd-navigation .square:focus {
  background: #ddd;
}

.game {
  display: flex;
  flex-direction: row;
}

.game-info {
  margin-left: 20px;
}

```

5. src 폴더에 index.js 추가
/src/index.js
```
class Square extends React.Component {
  render() {
    return (
      <button className="square">
        {/* TODO */}
      </button>
    );
  }
}

class Board extends React.Component {
  renderSquare(i) {
    return <Square />;
  }

  render() {
    const status = 'Next player: X';

    return (
      <div>
        <div className="status">{status}</div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}

class Game extends React.Component {
  render() {
    return (
      <div className="game">
        <div className="game-board">
          <Board />
        </div>
        <div className="game-info">
          <div>{/* status */}</div>
          <ol>{/* TODO */}</ol>
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);

```

6. src폴드의 index.js의 맨 위에 아래 코드 추가
```
import React from 'react';
import ReatDOM form 'react-dom';
import './index.css';
```

7. npm 서버 실행
```
npm start
```

http://localhost:3000 을 열면 빈 tic-tac-toe 필드 확인 가능



# Overview
## Inspecting the Starter Code

index.js에 3개 컴포넌트가 있는 것을 확인할 수 있다.
* Square
    * 버튼 렌더링
* Board
    * 9개 정사각형 렌더링
* Game
    * 보드 렌더링 (자리 표시 나중에 수정할 예정)

현재 컴포넌트간 상호작용은 없음 

## Passing Data Through Props

Board 컴포넌트에서 Square 컴포넌트로 데이터 전달

Board 컴포넌트의 renderSquer 메소드에서 Square로 value로 prop을 전달하기 위해 코드 수정

```
class Board extends React.Component{
    renderSquare(i){
        return <Square value={i} />;
    }
}
```

value를 보여주기 위해 {/* TODO */}를 {this.props.value}로 Square의 render 메소드 수정

```
class Square extends React.Component{
    render(){
        return {
            <button className="square">
                {this.props.value}
            </button>
        }
    }
}
```
  
각 렌더링 된 결과의 각 사각형에 숫자가 표시된다.

parent에서 child로 정보가 전달되는 방식을 알아봄.

## Making an Interactive Component

click 시 Square component를 "X"로 채운다 

먼저, Square 컴포넌트의 render() 함수에서 반환 된 버튼 태그를 아래와 같이 변경한다.

```
class Square extends React.Component{
    render() {
        return (
            <button className="square" onClick={() => alert("clcick")}>
                {this.props.value}
            </button>
        );
    }
}
```

다음으로 **state** 를 이용해 Square component 클릭 시 "X"로 마크한다. 


우선 클래스에 constructor를 추가해 state를 initialize 한다.

```
class Square extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            value: null,
        }
    }

    render(){
        return(
            <button className="square" onClick={()=>alert('click')}>
                {this.props.value}
            </button>
        )
    }
}
```

다음으로 클릭 시 현재 상태 값을 출력하기 위해 Square의 render method를 수정한다.

* this.props.value를 this.state.value로 변경
* () => alert() 이벤트 핸들러를 () => this.setSTate({value: 'X'}) 로 변경
* 가독성을 위해 className과 onClick 를 라인 나눔

위 작업 후에는 아래와 같아짐.
```
class Square extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            value:null,
        };
    }

    render() {
        return (
            <button
                className="square"
                onClick={()=>this.setState({value:"X"})}>
                {this.state.value}
            </button>
        )
    }
}
```
Square의 render 메소드에 있는 onClick 핸들러에서 this.setState를 호출하여 button을 클릭 할 때마다 React에 해당 Square를 다시 렌더링 하도록 지시한다. 업데이트가 끝나면 스퀘어의 this.state.value는 'X'가 되므로 게임 보드에 'X'가 표시된다. Square를 클릭하면 X가 나타난다.

(onClick을 누르면 setState가 호출이 되서 state값이 'X'로 바뀌기 때문에 Square에서 'X' 표시를 볼 수 있다. )


component에서 setState를  호출하면 React는 자동으로 내부의 하위 구성 요소도 업데이트 한다.


# Completing the Game

TODO
1. "X"랑 "O" 번갈아가면서 동작
2. winner 결정

## Why Immutability is important
위 예제에서 .slice()를 사용해 squares 의 복사본을 생성해서 array를 수정했다. 

이제 immutability와 immutability가 왜 중요한지 설명한다.

일반적으로 데이터를 변경하는데 두 가지 방법이 있다.
1. 데이터 값 직접 변경
```
var player = {score: 1, name: 'Jeff'}
player.score = 2;
// Now player is {score:2, name:'Jeff'}
```
2. 복사본 생성해서 데이터 대체
```
var player = {score:1, name:'Jeff'};
var newPlayer = Object.assign({}, player, {score:2});
//Player is unchanged, but newPlayer is {score:2, name:'Jeff'}

//Or if you are using objcet speread syntax proposal, you can write: 

// var newPlayer = {...player, score:2};
```

최종 결과는 동일하나, 몇 가지 이점을 얻을 수 있다.

1. 복잡한 기능이 간단 해짐
불변성으로 인해 복잡한 기능을 훨씬 쉽게 구현할 수 있다.

이 튜토리얼의 뒷부분에서 우리는 tic-tac-toe 게임의 역사를 검토하고 이전 동작으로 "뒤로 이동"할 수있는 "시간 이동"기능을 구현할 것인데, 이 기능은 응용 프로그램의 공통 요구 사항이다. 

직접적인 데이터 변이를 피함으로써 이전 버전의 게임 기록을 손상시키지 않고 나중에 재사용 할 수 있다.

2. 변화 감지.
변경 가능한 객체의 변경 사항을 감지하는 것은 직접 수정되기 때문에 어렵다.

**불변 객체의 변경을 감지하는 것은 상당히 쉽다. 참조 되고 있는 불변 개체가 이전 개체와 다른 경우 개체가 변경된 것이다.**

3. React에서 언제 Re-render할지 결정
immutability의 주요 이점은 React에서 순수한 구성 요소를 구축하는데 도움을 주는 것이다.

immutable data 데이터는 구성 요소의 재 렌더링이 필요한시기를 결정하는 데 도움이되는 변경 사항이 있는지 쉽게 판별 할 수 있다.

shouldComponentUpdate () 및 성능 최적화를 읽어 순수 구성 요소를 구축하는 방법에 대해 자세히 배울 수 있다.

## Functional Components

React에서 function component는 컴포넌트를 작성하는 간단한 방법이다.

render 메소드만 가지고, 자체 state는 가지지 않는다. React.Component 클래스 확장 대신에 props를 input으로 받아 렌더링해야하는 것을 반환하는 함수를 작성할 수 있다.

Square class를 아래 function으로 변경
```
function Square(props){
    return (
        <button className="square" onClick={props.onClick}>
            {props.value}
        </button>
    );
}
```

> Square를 Functional component로 변경할 때 onClick={()=>this.props.onClick()}을 onClick={props.onClick} 으로 변경했다. 클래스에서는 맞는 this 값을 접근하기 위해 arrow function을 사용했지만 functional component에서는 this에 대해 걱정할 필요가 없다.

## Taking Turns
"O" 처리

첫 번째는 'X'가 디폴트 값으로 설정한다. default 값은 Board constructor에서 설정할 수 있다.

```
class Board extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            squares: Array(9).fill(null),
            xIsNext:true,
        }
    }
}
```


플레이어가 움직일 때마다 xIsNext(a boolean)가 뒤집어서 다음 플레이어를 결정하고 게임의 상태가 저장된다. 보드의 handleClick 함수를 업데이트해서 xIsNext의 값을 변경한다.

```
handleClick(i){
    const squares = this.state.squares.slice();
    squares[i] = this.state.xIsNext ? 'X' : 'O';

    this.setState({
        squares:squares,
        xIsNext: !this.state.xIsNext,
    });
}
```

Board의 render에서 다음 차례가 누군지 'status' 텍스트도 변경한다.

```
render(){
    const status = 'Next player:' + (this.state.xIsNext ? 'X' : 'O')

    return(
        // the rest has not changed
```

변경사항 적용 후 Board component:
```
class Board extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            squares: Array(9).fill(null),
            xIsNext: true,
        };
    }

    handleClick(i){
        const squares = this.state.squares.slice();
        squares[i] = this.state.xIsNext ? 'X' : 'O';
        this.setState({
            squares: squares,
            xIsNext: !this.state.xIsNext,
        });
    }

    renderSquare(i){
        return (
            <Square
                value={this.state.squares[i]}
                onClick={() => this.handleClick(i)}
            />
        );
    }

    render(){
        const status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');

        return (
            <div>
                <div className="status">{status}</div>
                <div className="board-row">
                {this.renderSquare(0)}
                {this.renderSquare(1)}
                {this.renderSquare(2)}
                </div>
                <div className="board-row">
                {this.renderSquare(3)}
                {this.renderSquare(4)}
                {this.renderSquare(5)}
                </div>
                <div className="board-row">
                {this.renderSquare(6)}
                {this.renderSquare(7)}
                {this.renderSquare(8)}
                </div>
            </div>
        );
    }
}
```

## Declaring w Winner

누가 이겼는지, 더 이상 진행할 수 없는 상황인지 보여줘야 함.

아래 helper함수를 파일 맨 아래에 작성하여 winner를 정할 수 있다.

```
function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
```
Board의 render 함ㅅ수에서 calculateWinner(squares)를 호출해서 누가 이겼는지 체크할 수 있다. player가 이겼으면 "Winner: X" 나 "Winner: O"같은 텍스트를 출력할 수 있다. 


Board의 render함수의 status 를 아래 코드로 변경한다.
```
render() {
    const winner = calculateWinner(this.state.squares);

    let status;
    if (winner) {
        status = "Winner: " + winner;
    } else {
        status = "Next player: " + (this.state.xIsNext? 'X':'O')
    }

    return (
        // the rest has not changed
```

Board의 handleClick 함수를 변경하여 누군가가 게임에 이겼거나 스퀘어가 이미 채워진 경우 클릭을 무시하여 미리 return 한다.
```
handleClick(i){
    const squares = this.state.squares.slice();
    if (calculateWinner(squares) || squares[i]) {
        return;
    }

    squares[i] = this.state.xIsNext ? 'X' : 'O';
    this.setState({
      squares: squares,
      xIsNext: !this.state.xIsNext,
    });
}
```

# Adding Time Travel
