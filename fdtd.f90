program fdtd
    implicit none
    integer :: length, number_of_frames, steps_per_frame
    integer :: k, frame, step
    real :: c0, dz, tau, t0
    real :: dt, h1, h2, h3, e1, e2, e3
    real, allocatable, dimension(:) :: epsilon_r, mu_r, mE, mH, Ey, Hx
    real, allocatable, dimension(:) :: sourceEy, sourceHx
    character(len=20) :: filename, format_string

    ! Read parameters from CSV file
    open(1, file='parameters.csv', status='old')
    read(1,*) length, number_of_frames, steps_per_frame, c0, dz, tau, t0
    close(1)

    allocate(epsilon_r(length), mu_r(length), mE(length), mH(length))

    open(1, file='./materials/mu_r.csv', status='old')
    read(1,*) mu_r
    close(1)
    open(2, file='./materials/epsilon_r.csv', status='old')
    read(2,*) epsilon_r
    close(2)

    ! Compute update coefficients
    mE = 0.5*sqrt(epsilon_r(1)*mu_r(1))*dz/epsilon_r
    mH = 0.5*sqrt(epsilon_r(1)*mu_r(1))*dz/mu_r
    ! dt = n*dz/(2*c0)
    ! n := refractive index at boundries
    ! mE = c0*dt/epsilon_r = n*dz/(2*epsilon_r)
    ! mH = c0*dt/mu_r = n*dz/(2*mu_r)

    ! Compute time step
    dt = 0.5*sqrt(epsilon_r(1)*mu_r(1))*dz/c0

    deallocate(epsilon_r, mu_r)

    ! Initialize fields to zero
    allocate(Ey(length), Hx(length))
    do k=1, length
        Hx(k)=0
        Ey(k)=0
    end do

    ! Initialize boundary terms to zero
    h1=0;h2=0;h3=0
    e1=0;e2=0;e3=0

    ! Generate source
    allocate(sourceEy(number_of_frames*steps_per_frame))
    allocate(sourceHx(number_of_frames*steps_per_frame))
    do step=1, number_of_frames*steps_per_frame
        sourceEy(step)= exp(-((step*dt-t0)/tau)**2)
        sourceHx(step)= -exp(-(((step+1.5)*dt-t0)/tau)**2)
    end do

    ! Format for output
    format_string = 'E16.9'

    ! ------------------------ Main FDTD loop ------------------------ 
    do frame = 1, number_of_frames

        ! Run simulation up to next frame
        do step = 1, steps_per_frame

            ! Update H field
            do k = 1, length-1
                Hx(k) = Hx(k) + mH(k)*(Ey(k+1)-Ey(k))/dz
            end do
            Hx(length) = Hx(length) + mH(length)*(e3 - Ey(length))/dz
            ! Inject one-way source
            Hx(8) = Hx(8) - mH(8)*sourceEy(step+(frame-1)*steps_per_frame)/dz
            ! Handle boundary
            h3=h2; h2=h1; h1=Hx(1)


            ! Update E field
            Ey(1) = Ey(1) + mE(1)*(Hx(1) - h3)/dz
            do k = 2, length
                Ey(k) = Ey(k) + mE(k)*(Hx(k)-Hx(k-1))/dz
            end do
            ! Inject one-way source
            Ey(9) = Ey(9) - mE(9)*sourceHx(step+(frame-1)*steps_per_frame)/dz
            ! Handle boundary
            e3=e2; e2=e1; e1=Ey(length)

        end do


        ! Generate filename with frame number
        write (filename,'(I4.4".csv")') frame

        ! Write Hx to a CSV file
        open(1, file='./output/Hx'//filename, status='replace')
        do k = 1, length-1
            write(1,'('//format_string//'",")',advance='NO') Hx(k)
        end do
        write(1,'('//format_string//')',advance='NO') Hx(length)
        close(1)

        ! Write Ey to a CSV file
        open(2, file='./output/Ey'//filename, status='replace')
        write(2,'('//format_string//')',advance='NO') Ey(1)
        do k = 2, length
            write(2,'(","'//format_string//')',advance='NO') Ey(k)
        end do
        close(2)

    end do

end program fdtd