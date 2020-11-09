program fdtd
    implicit none
    integer, parameter :: length=4
    ! real, parameter :: c0=299792458.
    real, dimension(length) :: epsilon_r, mu_r, mE, mH, Ey, Hx
    real :: dz=1
    integer :: k, step, steps_per_frame=10, frame, number_of_frames=4
    character(len=20) :: filename, format_string='(E16.9)'
    ! Initialize materials to free space
    ! Initialize fields to zero
    do k=1, length
        epsilon_r(k)=1
        mu_r(k)=1

        Hx(k)=0
        Ey(k)=0
    end do
    
    ! Compute update coefficients

    ! dt = n*dz/(2*c0)
    ! n := refractive index at boundries
    ! mE = c0*dt/epsilon_r = n*dz/(2*epsilon_r)
    ! mH = c0*dt/mu_r = n*dz/(2*mu_r)

    mE = 0.5/epsilon_r
    mH = 0.5/mu_r

    ! Main FDTD loop
    do frame = 1, number_of_frames
        
        ! write (filename,*) frame
        print *, ''
        write (filename,'("frame"I4.4".csv")') frame
        print *, filename
        
        print *, ''

        do k = 1, length-1
            write(*,format_string,advance='NO') Hx(k)
            write(*,'(A)',advance='NO') ','
        end do
        write(*,format_string,advance='NO') Hx(1)
        
        print *, ''
        print *, ''

        write(*,format_string,advance='NO') Ey(1)
        do k = 2, length
            write(*,'(A)',advance='NO') ','
            write(*,format_string,advance='NO') Ey(k)
        end do

        print *, ''
        print *, ''

        do step = 1, steps_per_frame
            
            do k = 1, length-1
                Hx(k) = Hx(k) + mH(k)*(Ey(k+1)-Ey(k))/dz
            end do
            Hx(k) = Hx(k) - mH(k)*Ey(k)/dz

            Ey(k) = Ey(k) + mE(k)*Hx(k)/dz
            do k = 2, length
                Ey(k) = Ey(k) + mE(k)*(Hx(k)-Hx(k-1))/dz
            end do

        end do

    end do


end program fdtd

! function filename(n) result(name)
!     character(len=20) :: name
!     character(len=20) :: n2str
!     integer :: n
!     write (n2str,'(I4.4)') n
!     name = 'frame'//trim(n2str)//'.csv'
! end function filename

! function filename(n) result(name)
!     character(len=20) :: name
!     integer :: n
!     write (name,'("frame"I4.4".csv")') n
! end function filename