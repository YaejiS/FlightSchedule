from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import flight_client
from ..forms import SearchForm, ConfirmForm, ReviewForm
from ..models import User, Schedule, Review
from ..utils import current_time


flights = Blueprint('flights', __name__, static_folder='static',
                    template_folder='templates')


@flights.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("flights.query_results", country="us", originplace=form.originplace.data,
                                destinationplace=form.destinationplace.data,
                                outboundpartialdate=form.outboundpartialdate.data))

    return render_template("index.html", form=form)


@flights.route("/search-results/<country>&<originplace>&<destinationplace>&<outboundpartialdate>", methods=["GET"])
def query_results(country, originplace, destinationplace, outboundpartialdate):
    try:
        results = flight_client.search(country, originplace,
                                       destinationplace, outboundpartialdate)
    except ValueError as e:
        flash(str(e))
        # return redirect(url_for(""))
        return redirect(url_for("flights.index"))

    if len(results) == 0:
        flash("No flights found")
        return redirect(url_for("flights.index"))

    return render_template("query.html", results=results)


@flights.route("/flights/<minprice>&<originplace>&<destinationplace>&<outboundpartialdate>&<carrier>\
&<originairport>&<destinationairport>", methods=["GET", "POST"])
def flight_detail(minprice, originplace, destinationplace, outboundpartialdate, carrier, originairport, destinationairport):
    if current_user.is_authenticated == False:
        return redirect(url_for("users.login"))

    form = ConfirmForm()
    detail = {}
    detail["country"] = "US"
    detail["originplace"] = originplace
    detail["destinationplace"] = destinationplace
    detail["outboundpartialdate"] = outboundpartialdate
    detail["minprice"] = minprice
    detail["carrier"] = carrier
    detail["originairport"] = originairport
    detail["destinationairport"] = destinationairport
    if form.validate_on_submit() and current_user.is_authenticated:
        schedule = Schedule(
            traveller=current_user._get_current_object(),
            originplace=originplace,
            destinationplace=destinationplace,
            departure_date=outboundpartialdate,
            price=minprice,
            carrier=carrier
        )
        schedule.save()
        return redirect(url_for("flights.user_detail", username=current_user._get_current_object().username))

    schedules = Schedule.objects(traveller=current_user._get_current_object())

    return render_template(
        "flight_detail.html", form=form, detail=detail
    )


@flights.route("/reviews/<carrier>", methods=["GET", "POST"])
def carrier_detail(carrier):
    if current_user.is_authenticated == False:
        return redirect(url_for("users.login"))

    form = ReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            carrier=carrier,
        )
        review.save()
        return redirect(request.path)

    reviews = Review.objects(carrier=carrier)

    return render_template(
        "carrier_detail.html", form=form, carrier=carrier, reviews=reviews
    )


@flights.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    schedules = Schedule.objects(traveller=user)
    reviews = Review.objects(commenter=user)

    return render_template("user_detail.html", username=username, schedules=schedules, reviews=reviews)
