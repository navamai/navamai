Now that you know a little more about all the individual pieces, let's close the loop and review how it works together:

  1. Streamlit apps are Python scripts that run from top to bottom.
  2. Every time a user opens a browser tab pointing to your app, the script is executed and a new session starts.
  3. As the script executes, Streamlit draws its output live in a browser.
  4. Every time a user interacts with a widget, your script is re-executed and Streamlit redraws its output in the browser. 
     * The output value of that widget matches the new value during that rerun.
  5. Scripts use the Streamlit cache to avoid recomputing expensive functions, so updates happen very fast.
  6. Session State lets you save information that persists between reruns when you need more than a simple widget.
  7. Streamlit apps can contain multiple pages, which are defined in separate `.py` files in a `pages` folder.

_forum_

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.
