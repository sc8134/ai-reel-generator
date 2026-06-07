from flask import Blueprint, request, jsonify
from services.template_generator import (
    ALL_TEMPLATES,
    get_categories,
    get_color_schemes,
    get_styles,
)

templates_bp = Blueprint("templates", __name__)

PAGE_SIZE = 40  # templates per page


@templates_bp.route("/api/templates", methods=["GET"])
def get_templates():
    """
    GET /api/templates
    Query params:
      - page      (int, default 1)
      - category  (str, filter by category key)
      - scheme    (str, filter by color scheme name)
      - style     (str, filter by style name)
      - q         (str, search in name/description)
    Returns paginated templates + total count + filter options.
    """
    page = max(1, int(request.args.get("page", 1)))
    category = request.args.get("category", "").strip().lower()
    scheme = request.args.get("scheme", "").strip().lower()
    style = request.args.get("style", "").strip().lower()
    query = request.args.get("q", "").strip().lower()

    filtered = ALL_TEMPLATES

    if category:
        filtered = [t for t in filtered if t["category"] == category]
    if scheme:
        filtered = [t for t in filtered if t["color_scheme"].lower() == scheme]
    if style:
        filtered = [t for t in filtered if t["style"].lower() == style]
    if query:
        filtered = [
            t for t in filtered
            if query in t["name"].lower() or query in t["description"].lower()
        ]

    total = len(filtered)
    start = (page - 1) * PAGE_SIZE
    page_items = filtered[start: start + PAGE_SIZE]

    return jsonify({
        "templates": page_items,
        "total": total,
        "page": page,
        "page_size": PAGE_SIZE,
        "total_pages": (total + PAGE_SIZE - 1) // PAGE_SIZE,
        "filters": {
            "categories": get_categories(),
            "color_schemes": get_color_schemes(),
            "styles": get_styles(),
        },
    })


@templates_bp.route("/api/templates/<template_id>", methods=["GET"])
def get_template(template_id: str):
    from services.template_generator import get_template_by_id
    t = get_template_by_id(template_id)
    return jsonify(t)
