def site_settings(request):
    default_color = "#ffffed"
    return {
        "background_color": request.session.get(
            "background_color", default_color
        )
    }
