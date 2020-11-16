program fdtd
    implicit none
    integer, parameter :: length=120, number_of_frames=90, steps_per_frame=3
    integer :: k, frame, step
    real, parameter :: c0=1, dz=1
    real, dimension(length) :: epsilon_r, mu_r, mE, mH, Ey, Hx
    real, dimension(number_of_frames*steps_per_frame) :: source
    real :: dt, h1, h2, h3, e1, e2, e3
    character(len=20) :: filename, format_string

    ! Compute time step
    dt = 0.5*dz/c0

    do k=1, length
        ! Initialize materials to free space
        epsilon_r(k)=1
        mu_r(k)=1

        ! Initialize fields to zero
        Hx(k)=0
        Ey(k)=0
    end do

    ! Initialize boundary terms to zero
    h1=0;h2=0;h3=0
    e1=0;e2=0;e3=0

    ! Generate source
    do step=1, number_of_frames*steps_per_frame
        source(step)= exp(-((step*dt-24)/6)**2)
    end do


    ! Compute update coefficients
    mE = 0.5*dz/epsilon_r
    mH = 0.5*dz/mu_r
    
    ! dt = n*dz/(2*c0)
    ! n := refractive index at boundries
    ! mE = c0*dt/epsilon_r = n*dz/(2*epsilon_r)
    ! mH = c0*dt/mu_r = n*dz/(2*mu_r)


    ! Format for output
    format_string = 'E16.9'

    ! ---------------- Main FDTD loop ---------------- 
    do frame = 1, number_of_frames

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


        ! Run simulation up to next frame
        do step = 1, steps_per_frame
            ! Update Hx
            do k = 1, length-1
                Hx(k) = Hx(k) + mH(k)*(Ey(k+1)-Ey(k))/dz
            end do
            Hx(length) = Hx(length) + mH(length)*(e3 - Ey(length))/dz
            h3=h2; h2=h1; h1=Hx(1)

            ! Update Ey
            Ey(1) = Ey(1) + mE(1)*(Hx(1) - h3)/dz
            do k = 2, length
                Ey(k) = Ey(k) + mE(k)*(Hx(k)-Hx(k-1))/dz
            end do
            e3=e2; e2=e1; e1=Ey(length)

            ! Inject source
            Ey(40) = Ey(40) + source(step + (frame-1)*steps_per_frame)
        end do

    end do


end program fdtd