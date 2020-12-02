from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import flight_client
from ..forms import SearchForm, ConfirmForm
from ..models import User, Schedule
from ..utils import current_time


flights = Blueprint('flights', __name__, static_folder='static',
                    template_folder='templates')


@flights.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("flights.query_results", country=form.country.data, originplace=form.originplace.data,
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

    return render_template("query.html", results=results)


@flights.route("/flights/<minprice>&<originplace>&<destinationplace>&<outboundpartialdate>", methods=["GET", "POST"])
def flight_detail(minprice, originplace, destinationplace, outboundpartialdate):
    try:
        print(minprice)
        print("--------")
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("users.login"))

    form = ConfirmForm()
    detail = {}
    detail["country"] = "US"
    detail["originplace"] = originplace
    detail["destinationplace"] = destinationplace
    detail["outboundpartialdate"] = outboundpartialdate
    detail["minprice"] = minprice
    if form.validate_on_submit() and current_user.is_authenticated:
        schedule = Schedule(
            traveller=current_user._get_current_object(),
            originplace=originplace,
            destinationplace=destinationplace,
            departure_date=outboundpartialdate,
            price=minprice
        )
        schedule.save()
        return redirect(url_for("flights.user_detail", username=current_user._get_current_object().username))

    schedules = Schedule.objects(traveller=current_user._get_current_object())

    return render_template(
        "flight_detail.html", form=form, detail=detail
    )


@flights.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    schedules = Schedule.objects(traveller=user)

    return render_template("user_detail.html", username=username, schedules=schedules)
