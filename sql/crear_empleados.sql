create table empleados(
    cedula varchar(20) primary key,
    fecha_ingreso DATE not NULL,
    fecha_salida DATE not NULL,
    salario int not null,
    cesantias float not null,
    interes_cesantias float not null,
    vacaciones float not null,
    prima_servicios float not null,
    pago_neto float not null
    
);

