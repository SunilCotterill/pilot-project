import streamlit as st
from typing import Any, Dict, List


def matches(data: Any, term: str) -> bool:
    """
    Recursively check if search term appears in key or value of JSON data.
    """
    term = term.lower()
    if isinstance(data, dict):
        return any(term in str(k).lower() or matches(v, term) for k, v in data.items())
    if isinstance(data, list):
        return any(matches(item, term) for item in data)
    return term in str(data).lower()

def set_in(data, path, value):
    """
    Update value in JSON 
    """
    for key in path[:-1]:
        data = data[key]
    data[path[-1]] = value


def get_in(data, path):
    """
    Retrieve a value by path
    """
    for key in path:
        data = data[key]
    return data

def filter_json(data: Any, term: str) -> Any:
    """
    Return a pruned copy of data where only matching nodes are kept.
    """
    if not term:
        return data
    if isinstance(data, dict):
        new_dict: Dict[Any, Any] = {}
        for k, v in data.items():
            if term.lower() in str(k).lower() or matches(v, term):
                new_dict[k] = v
        return new_dict
    if isinstance(data, list):
        filtered_list: List[Any] = []
        for item in data:
            if matches(item, term):
                filtered_list.append(filter_json(item, term))
        return filtered_list
    return data

def render_json(
    data: Any,
    key: str = None,
    path = None
) -> Any:
    
    """
    Recursively render JSON data as editable
    """
    path = path or []

    if isinstance(data, dict):
        container = st.expander(key, expanded = True) if key else st.container()
        new_dict = {}
        with container:
            for k, v in data.items():
                new_dict[k] = render_json(v, k, path+[k])
        return new_dict

    elif isinstance(data, list):
        if data and all(isinstance(el, dict) for el in data):
            keys0 = set(data[0].keys())
            if all(set(el.keys()) == keys0 for el in data):
                import pandas as pd

                df = pd.DataFrame(data)
                if key:
                    st.markdown(f"**{key}**")
                edited_df = st.data_editor(
                    df,
                    num_rows="dynamic",
                    key=path
                )

                for row_idx, row in edited_df.iterrows():
                    for col in edited_df.columns:
                        set_in(
                            st.session_state.data,
                            path + [row_idx, col],
                            row[col]
                        )

                return st.session_state.data if not path else get_in(st.session_state.data, path)

        container = st.expander(f"{key} [{len(data)}]") if key else st
        new_list = []
        with container:
            for idx, item in enumerate(data):
                new_list.append(render_json(item, f"[{idx}]", path+[idx]))
        return new_list

    else:
        widget_key = ".".join(map(str, path))
        # TODO: Add different field 
        # if isinstance(data, bool):
        #     val = st.checkbox(
        #         label=key or "",
        #         value=data,
        #         key=widget_key
        #     )

        # # ints / floats
        # elif isinstance(data, int):
        #     val = st.number_input(
        #         label=key or "",
        #         value=data,
        #         step=1,
        #         key=widget_key
        #     )
        # elif isinstance(data, float):
        #     val = st.number_input(
        #         label=key or "",
        #         value=data,
        #         key=widget_key
        #     )

        # # everything else → string
        # else:
        val =  st.text_input(
            label=key or "",
            value=str(data),
            key=widget_key
        )
    set_in(st.session_state.data, path, val)
