"""rocketlib — OpenRocket 24.12 üzerine headless roket tasarım kütüphanesi.

Tüm dışa açık fonksiyonlarda **SI birimleri** kullanılır: uzunluk metre,
kütle kg, hız m/s, sıcaklık K, basınç Pa. Açılar **derece** verilir
(OpenRocket'ın Java API'si radyan bekler, dönüşüm kütüphane içinde yapılır).

Hızlı başlangıç::

    import rocketlib

    doc = rocketlib.new_design("Mini roket")
    rocketlib.add_nose_cone(doc, length=0.10, radius=0.019)
    rocketlib.add_body_tube(doc, length=0.30, radius=0.019)
    rocketlib.add_fin_set(doc, count=3, root_chord=0.05, tip_chord=0.02,
                          height=0.03, sweep=45.0)
    rocketlib.add_inner_tube(doc, length=0.07, radius=0.0125)
    rocketlib.add_parachute(doc, diameter=0.30)
    rocketlib.add_shock_cord(doc, length=0.30)
    rocketlib.set_launch_conditions(doc, rod_length=1.0, rod_angle=18.0, wind_speed=3.0)
    rocketlib.set_motor(doc, "C6", manufacturer="Estes")
    print(rocketlib.run(doc, seed=1)["apogee_m"])
    for issue in rocketlib.validate(doc):
        print(issue)
"""

from .build import (
    add_body_tube,
    add_fin_set,
    add_inner_tube,
    add_mass_component,
    add_nose_cone,
    add_parachute,
    add_shock_cord,
    add_stage,
    add_transition,
    find_component,
    list_components,
    move_component,
    remove_component,
    set_bulkhead_thickness,
    set_centering_ring_thickness,
    set_component_material,
    set_component_position,
    set_parachute_deployment,
    set_nose_shoulder,
    set_surface_finish,
    update_component,
)
from .detail import (
    add_bulkhead,
    add_centering_ring,
    add_rail_button,
    add_tube_coupler,
    set_parachute_packed,
    set_stage_separation,
)
from .errors import (
    ComponentNotFoundError,
    DesignError,
    DuplicateComponentError,
    MotorError,
    RocketLibError,
    SessionError,
    SimulationError,
    ValidationError,
)
from .inspect import inspect_component, inspect_design
from .io import (
    copy_design,
    load_design,
    new_design,
    save_design,
    save_design_with_data,
)
from .launch import get_motor, set_launch_conditions, set_motor, set_motor_ignition
from .run import METRIC_UNITS, run
from .session import get_session, session_info, start_session
from .validate import validate

__version__ = "1.0.0"

__all__ = [
    # oturum
    "start_session",
    "get_session",
    "session_info",
    # dosya
    "load_design",
    "save_design",
    "save_design_with_data",
    "copy_design",
    "new_design",
    # inceleme
    "inspect_design",
    "inspect_component",
    # kurulum
    "add_nose_cone",
    "add_body_tube",
    "add_transition",
    "add_fin_set",
    "add_inner_tube",
    "add_mass_component",
    "add_parachute",
    "add_shock_cord",
    "add_stage",
    "move_component",
    "update_component",
    "remove_component",
    "find_component",
    "list_components",
    # malzeme / konum
    "set_bulkhead_thickness",
    "set_centering_ring_thickness",
    "set_component_material",
    "set_surface_finish",
    "add_centering_ring",
    "add_bulkhead",
    "add_tube_coupler",
    "add_rail_button",
    "set_parachute_packed",
    "set_stage_separation",
    "set_nose_shoulder",
    "set_component_position",
    "set_parachute_deployment",
    # fırlatma
    "set_launch_conditions",
    "set_motor",
    "get_motor",
    "set_motor_ignition",
    # simülasyon
    "run",
    "METRIC_UNITS",
    # doğrulama
    "validate",
    # hatalar
    "RocketLibError",
    "SessionError",
    "DesignError",
    "ComponentNotFoundError",
    "DuplicateComponentError",
    "MotorError",
    "SimulationError",
    "ValidationError",
    "__version__",
]
