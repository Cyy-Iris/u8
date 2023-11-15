def convert_page_to_snippets(page):
    lines = page.strip().split("\n")

    # get title hierarchy
    title_inds = []
    for ind, line in enumerate(lines):
        if line.startswith("#"):
            title_inds.append(ind)

    snippets = []
    title_hierarchy = []
    current_clause = []

    for line in lines:
        if line.startswith("#"):
            if current_clause:
                # end of current clause
                snippet = render_clause(current_clause, title_hierarchy)
                if snippet:
                    snippets.append(snippet)

                current_clause = []

            title_hierarchy.append(line)
        else:
            current_clause.append(line)

    if current_clause:
        snippet = render_clause(current_clause, title_hierarchy)
        if snippet:
            snippets.append(snippet)

    return snippets


def render_clause(clause, titles):
    max_lvl = 5
    selected_titles = []

    for title in reversed(titles):
        lvl = get_title_level(title)
        if max_lvl > lvl:
            max_lvl = lvl
            selected_titles.insert(0, title)

    render_text = "\n".join(selected_titles + clause)

    # handle empty clauses
    if not "".join(clause).strip():
        # make an exception for 'List item'; sometimes content is empty but present in the title.
        if "List item" not in render_text:
            return None

    return render_text


def get_title_level(s):
    return len(s) - len(s.lstrip("#"))
