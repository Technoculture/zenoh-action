import { useState, useEffect } from "react";
import './App.css';
import axios from 'axios';
import { ToastContainer, Flip, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Graphviz from 'graphviz-react';
import action from "./data/action.json";
import statechart from "./data/statechart.json";

const actionsList = new Set(action.actions);
const statesList = new Set(action.states);
const endpointsList = new Set([...actionsList, ...statesList, "status"]);

const url = action.base_url;
const key_expression = action.key_expression;

function endpoint_url(endpoint = "") {
    if (endpointsList.has(endpoint)) {
        return `${url}/${key_expression}/${endpoint}`;
    } else if (endpoint === "") {
        return `${url}/${key_expression}`;
    } else {
        throw TypeError(`Declaration for Endpoint(${endpoint}) is not present in the action.json file`);
    }
}

function states(json) {
	let _states = {};

	json.states.map(state => {
		_states[state.name] = (state.children && state.children.length != 0) || false;

		if (state.children) {
			state.children.map(child => {
				_states[child.name] = (child.children && child.children.length != 0) || false;
			});
		}
	});

	return _states;
}

function children_of(json, state) {
	return [];
}
function transitions(json) {
	let _transitions = [];

	json.transitions.map(transition => {
		_transitions.push(transition)
	})

	json.states.map(state => {
		state.children && state.children.map(substate => {
			substate.transitions && substate.transitions.map(transition => {
				_transitions.push(transition)
			})
		})
	})

	// console.log(_transitions);
	return _transitions;
}

function childtransitionToStr(json, cluster) {
	let child_transition = "";
	json.states.map(state => {
		if (cluster == state.name) {
			state.transitions.map(transition => {
				child_transition += transitionToStr(transition, cluster);
			});
    }
  })
	return child_transition;
}

function transitionToStr(transition, state_list) {
	let cluster_label = "";
	if (state_list[transition.dest]) {
		// console.log(`${transition.dest} has children.`);
		cluster_label += `, ltail=${transition.dest}`;
	}
	if (state_list[transition.source]) {
		// console.log(`${transition.source} has children.`);
		cluster_label += `, lhead=${transition.source}`;
	}
	return `"${transition.source}" -> "${transition.dest}" [label="${transition.trigger} ${cluster_label}"]\n`;
}

function generateDotFile(json, current_state) {
	let dot = "digraph {\n";
	dot += `rankdir=LR;\n`;
	dot += `Entry [shape="point" label=""]`;
	dot += `Entry -> ${json.initial}\n`;
  	dot += `${json.initial} [shape=ellipse, color=red, fillcolor= orangered3, fontcolor=black, style=filled]; \n`;
	// Approach 1: Build some data structures, then draw
	let state_dict = states(statechart);
	let transition_list = transitions(statechart);

	console.log(state_dict)
	console.log(transition_list);

	const clusters = [];
	Object.entries(state_dict)
		.filter(([k, v]) => v === true)
		.map(arr => clusters.push(arr[0]));
	console.log(clusters);

	clusters.map(cluster => {
		dot += `subgraph cluster_${cluster} {\n`;
    dot += `${current_state} [shape=ellipse, color=lightsalmon, fillcolor=lightsalmon, fontcolor=black, style=filled]; \n`;
		dot +=   childtransitionToStr(json, cluster);
		dot += ` label=${cluster}\n`;

		children_of(cluster).map(state => {
			dot += `  ${state}\n`;

		})

		dot += `}\n`;
	})

	transition_list.map(transition => {
		dot += transitionToStr(transition, state_dict);
	})

	dot += "}\n";
	return dot;
}

const ActionComponent = () => {
    let [actionStatus, setStatus] = useState("Unknown");

    useEffect(() => {
        const sse = new EventSource(endpoint_url("listen"));

        sse.addEventListener("PUT", (e) => {
            const value = JSON.parse(e.data).value;
            if (value !== actionStatus) {
                setStatus(value); 
            }
        });
    });

    const postAction = async (action, payload = '') => {
        if (actionsList.has(action)) {
            try {
                const response = await axios.post(endpoint_url(action), payload, {
                    headers: {
                        'Content-Type': 'application/text'
                    }
                });
                toast.success(`Action dispatched: ${action}`);
                return response.data;
            } catch (error) {
                toast.error(error.message);
                throw error;
            } 
        } else {
            const errmsg = `Action(${action}) not supported.`;
            toast.error(errmsg);
            throw errmsg;
        }
    };

    return (
        <div>
            <h3>Status</h3>
            <p>{actionStatus}</p>

            <h3>Action Buttons</h3>
            <button onClick={() => postAction("start", "started")}>Start</button>
            <button onClick={() => postAction("stop", "stopped")}>Stop</button>

            <button onClick={() => postAction("hello")}>Hello</button>
        </div>
    );
}

function App() {
    const dot = generateDotFile(statechart, "busy");
  return (
    <div className="App">
        <header className="App-header">
            <h1>Action Dashboard</h1>
            <h3>Action Endpoint</h3>
            <p>{endpoint_url()}</p>
        </header>
		<div>
			<Graphviz dot={dot} />
			<p>{dot}</p>
		</div>
        <ToastContainer 
            autoClose={1000}
            transition={Flip}
            hideProgressBar={false}
            pauseOnFocusLoss={false}
            newestOnTop={true}
            pauseOnHover={false}
        />
        <ActionComponent />
    </div>
  );
}

export default App;
