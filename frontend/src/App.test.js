import React from "react";
import { act } from "react-dom/test-utils";
import Result from "./result"
import Form from "./form"
import getSearch from "./form"
import { unmountComponentAtNode } from "react-dom";
import { render, screen } from '@testing-library/react';


let container = null;
beforeEach(() => {
  // setup a DOM element as a render target
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  // cleanup on exiting
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});

it ("test form", async () => {
  await act(async () => {
    render(<Form />, container);
  });
  let query = screen.getByRole("textbox", {
    name: "Query:"
  })
  let limit = screen.getByRole("spinbutton", {
    name : "Number of Results:"
  })
  let algo = screen.getByRole("combobox", {
    name : 'Search Algorithm:'
  })

  
  query.value = "communism";
  limit.value = 10;
  algo.value = "tfidf"

  expect(query).toHaveValue("communism");
  expect(limit).toHaveValue(10);
  expect(algo).toHaveValue("tfidf");
})

it ("test tfidf api", async () => {
  await act(async () => {
    render(<Form />, container);
  });
  let query = screen.getByRole("textbox", {
    name: "Query:"
  })
  let limit = screen.getByRole("spinbutton", {
    name : "Number of Results:"
  })
  let algo = screen.getByRole("combobox", {
    name : 'Search Algorithm:'
  })

  query.value = "communism";
  limit.value = 1;
  algo.value = "tfidf"
  const data = [[2, 0.32776067582934276]]
  var api = "http://localhost:5000/search?" + new URLSearchParams({
            query : query.value,
            limit : limit.value,
            searchAlgo: algo.value
  });
  await fetch(api, {
    method : "GET",
  }).then(r => r.json()).then(
    d => {
      expect(d["Status"]).toEqual(200);
      expect(d["results"]).toEqual(data);
    }
  )
})
it ("test ratcliff api", async () => {
  await act(async () => {
    render(<Form />, container);
  });
  let query = screen.getByRole("textbox", {
    name: "Query:"
  })
  let limit = screen.getByRole("spinbutton", {
    name : "Number of Results:"
  })
  let algo = screen.getByRole("combobox", {
    name : 'Search Algorithm:'
  })

  query.value = "communism";
  limit.value = 3;
  algo.value = "ratcliff"
  const data = [['Christian_communism.txt', 0.9729323308270676], ['Bushyhead_Oklahoma.txt', 0.9602649006622517], ['NGC_2613.txt', 0.9566265060240964]]
  var api = "http://localhost:5000/search?" + new URLSearchParams({
            query : query.value,
            limit : limit.value,
            searchAlgo: algo.value
  });
  await fetch(api, {
    method : "GET",
  }).then(r => r.json()).then(
    d => {
      expect(d["Status"]).toEqual(200);
      expect(d["results"]).toEqual(data);
    }
  )
})